from __future__ import annotations

from typing import Any


REPLICATION_AUDIT_SCHEMA = "primeproject.replication-audit.v1"


def build_replication_audit(
    *,
    attribution_grid: dict[str, Any],
    null_calibration: dict[str, Any] | None = None,
    lift_threshold: float = 0.10,
    minimum_replicated_ratio: float = 0.75,
) -> dict[str, Any]:
    if not 0 <= lift_threshold <= 1:
        raise ValueError("lift_threshold must be between 0 and 1")
    if not 0 < minimum_replicated_ratio <= 1:
        raise ValueError("minimum_replicated_ratio must be in (0, 1]")

    random_baseline = float(attribution_grid.get("random_baseline_accuracy", 0.0) or 0.0)
    if not 0 < random_baseline < 1:
        raise ValueError("attribution grid must include a random_baseline_accuracy between 0 and 1")

    deltas = attribution_grid.get("deltas", []) or []
    if not deltas:
        raise ValueError("attribution grid must include confound deltas")

    null_profiles = {
        profile.get("profile"): profile
        for profile in (null_calibration or {}).get("profiles", [])
    }
    by_profile: dict[str, list[dict[str, Any]]] = {}
    for delta in deltas:
        by_profile.setdefault(str(delta.get("profile")), []).append(delta)

    profile_reports = []
    setting_reports = []
    for profile, profile_deltas in sorted(by_profile.items()):
        grouped = group_by_setting(profile_deltas)
        settings = []
        replicated_count = 0
        weak_settings = []
        for setting, setting_deltas in sorted(grouped.items()):
            controlled_values = [float(delta.get("controlled_accuracy", 0.0) or 0.0) for delta in setting_deltas]
            lift_values = [value - random_baseline for value in controlled_values]
            setting_mean = mean(controlled_values)
            setting_lift = setting_mean - random_baseline
            replicated = setting_lift >= lift_threshold
            if replicated:
                replicated_count += 1
            else:
                weak_settings.append(setting)
            setting_report = {
                "profile": profile,
                "setting": setting,
                "repeat_count": len(setting_deltas),
                "mean_controlled_accuracy": round_float(setting_mean),
                "min_controlled_accuracy": round_float(min(controlled_values) if controlled_values else 0.0),
                "max_controlled_accuracy": round_float(max(controlled_values) if controlled_values else 0.0),
                "mean_lift": round_float(setting_lift),
                "min_lift": round_float(min(lift_values) if lift_values else 0.0),
                "status": "replicated" if replicated else "weak",
            }
            settings.append(setting_report)
            setting_reports.append(setting_report)

        setting_count = len(settings)
        replicated_ratio = replicated_count / setting_count if setting_count else 0.0
        null_profile = null_profiles.get(profile, {})
        null_status = null_profile.get("interpretation", "not_calibrated")
        status = interpret_profile(
            replicated_ratio=replicated_ratio,
            minimum_replicated_ratio=minimum_replicated_ratio,
            null_status=str(null_status),
        )
        profile_reports.append(
            {
                "profile": profile,
                "setting_count": setting_count,
                "replicated_setting_count": replicated_count,
                "replicated_ratio": round_float(replicated_ratio),
                "mean_controlled_accuracy": round_float(mean([item["mean_controlled_accuracy"] for item in settings])),
                "minimum_setting_lift": round_float(min([item["mean_lift"] for item in settings]) if settings else 0.0),
                "null_interpretation": null_status,
                "familywise_p_value": null_profile.get("familywise_p_value"),
                "status": status,
                "weak_settings": weak_settings,
            }
        )

    profile_reports.sort(
        key=lambda item: (
            item["status"] != "replicated_and_null_calibrated",
            -float(item["replicated_ratio"]),
            -float(item["mean_controlled_accuracy"]),
        )
    )
    stable_profiles = [
        profile["profile"]
        for profile in profile_reports
        if profile["status"] == "replicated_and_null_calibrated"
    ]
    return {
        "schema": REPLICATION_AUDIT_SCHEMA,
        "source": {
            "attribution_grid_schema": attribution_grid.get("schema"),
            "null_calibration_schema": (null_calibration or {}).get("schema"),
            "random_baseline_accuracy": random_baseline,
        },
        "method": {
            "name": "setting-level replication audit",
            "lift_threshold": lift_threshold,
            "minimum_replicated_ratio": minimum_replicated_ratio,
            "interpretation": "A profile is stable only when it repeats across limit/train/test settings and survives null calibration.",
        },
        "summary": {
            "profile_count": len(profile_reports),
            "setting_count": len({row["setting"] for row in setting_reports}),
            "stable_profile_count": len(stable_profiles),
            "stable_profiles": stable_profiles,
            "claim_floor": "controlled_synthetic_only",
        },
        "profiles": profile_reports,
        "settings": setting_reports,
    }


def group_by_setting(deltas: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for delta in deltas:
        setting = str(delta.get("base_pair_key") or delta.get("pair_key") or "unknown")
        grouped.setdefault(setting, []).append(delta)
    return grouped


def interpret_profile(
    *,
    replicated_ratio: float,
    minimum_replicated_ratio: float,
    null_status: str,
) -> str:
    replicated = replicated_ratio >= minimum_replicated_ratio
    null_survives = null_status == "familywise_survives_null"
    if replicated and null_survives:
        return "replicated_and_null_calibrated"
    if replicated:
        return "replicated_but_null_limited"
    if null_survives:
        return "null_survives_but_setting_fragile"
    return "not_replicated"


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def round_float(value: Any) -> float:
    try:
        return round(float(value), 6)
    except (TypeError, ValueError):
        return 0.0
