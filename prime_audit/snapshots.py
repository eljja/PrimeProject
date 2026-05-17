from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from html import escape
from json import dumps
from math import gcd, log2
from pathlib import Path
from typing import Any

from .conjecture_lab import sieve_primes


GENERATORS = ("next_prime", "rejection", "wheel30_next")
GENERATOR_COLORS = {
    "next_prime": "#087f7a",
    "rejection": "#d78a11",
    "wheel30_next": "#4657d8",
}
WHEEL_30_RESIDUES = {1, 7, 11, 13, 17, 19, 23, 29}


@dataclass
class Accumulator:
    total_weight: float = 0.0
    weighted_gap_sum: float = 0.0
    weight_log_sum: float = 0.0
    max_weight: float = 0.0

    def add(self, weight: float, gap: int) -> None:
        self.total_weight += weight
        self.weighted_gap_sum += weight * gap
        if weight > 0:
            self.weight_log_sum += weight * log2(weight)
        self.max_weight = max(self.max_weight, weight)

    def summary(self) -> dict[str, float]:
        entropy = log2(self.total_weight) - (self.weight_log_sum / self.total_weight)
        return {
            "total_weight": self.total_weight,
            "entropy_bits": entropy,
            "effective_support": 2**entropy,
            "max_weight_share": self.max_weight / self.total_weight,
            "weighted_mean_gap": self.weighted_gap_sum / self.total_weight,
        }


def build_snapshot(limit: int, modulo: int = 210, bins: int = 48) -> dict[str, Any]:
    primes = sieve_primes(limit)
    if len(primes) < 2:
        raise ValueError("limit must contain at least two primes")

    gaps = [prime - previous for previous, prime in zip(primes, primes[1:])]
    max_gap = max(gaps)
    max_gap_index = gaps.index(max_gap) + 1
    mean_gap = sum(gaps) / len(gaps)
    residues = [residue for residue in range(modulo) if gcd(residue, modulo) == 1]
    residue_index = {residue: index for index, residue in enumerate(residues)}

    accumulators = {generator: Accumulator() for generator in GENERATORS}
    residue_totals = {
        generator: [0.0 for _ in residues]
        for generator in GENERATORS
    }
    histograms = {
        generator: [0.0 for _ in range(bins)]
        for generator in GENERATORS
    }
    tail_events: list[dict[str, int]] = []

    for previous, prime, gap in zip(primes, primes[1:], gaps):
        weights = {
            "next_prime": gap,
            "rejection": 1,
            "wheel30_next": _wheel30_count(previous, prime),
        }
        bin_index = min(bins - 1, int((gap / (max_gap + 1)) * bins))
        residue = prime % modulo
        for generator, weight in weights.items():
            accumulators[generator].add(weight, gap)
            histograms[generator][bin_index] += weight
            if residue in residue_index:
                residue_totals[generator][residue_index[residue]] += weight
        if gap >= max_gap * 0.75:
            tail_events.append({"previous_prime": previous, "prime": prime, "gap": gap})

    generator_summaries: dict[str, dict[str, Any]] = {}
    uniform = 1 / len(residues)
    for generator in GENERATORS:
        total = accumulators[generator].total_weight
        distribution = [
            {
                "residue": residue,
                "mass": residue_totals[generator][index] / total,
            }
            for index, residue in enumerate(residues)
        ]
        tv = 0.5 * sum(abs(item["mass"] - uniform) for item in distribution)
        histogram_total = sum(histograms[generator])
        generator_summaries[generator] = {
            **accumulators[generator].summary(),
            "residue_total_variation": tv,
            "residue_distribution": distribution,
            "gap_histogram": [
                {
                    "start": int((index / bins) * max_gap),
                    "end": int(((index + 1) / bins) * max_gap),
                    "mass": value / histogram_total if histogram_total else 0.0,
                }
                for index, value in enumerate(histograms[generator])
            ],
        }

    return {
        "schema": "primeproject.snapshot.v1",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "limit": limit,
        "modulo": modulo,
        "bins": bins,
        "prime_count": len(primes),
        "observation_count": len(gaps),
        "max_prime": primes[-1],
        "max_gap": max_gap,
        "max_gap_event": {
            "previous_prime": primes[max_gap_index - 1],
            "prime": primes[max_gap_index],
            "gap": max_gap,
        },
        "mean_gap": mean_gap,
        "tail_events": sorted(tail_events, key=lambda item: item["gap"], reverse=True)[:20],
        "generators": generator_summaries,
    }


def write_snapshot(snapshot: dict[str, Any], output: str | Path) -> None:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dumps(snapshot, indent=2), encoding="utf-8")


def render_snapshot_svgs(snapshot: dict[str, Any], out_dir: str | Path, slug: str | None = None) -> list[Path]:
    output_dir = Path(out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    name = slug or f"prime_measure_{_compact_limit(snapshot['limit'])}"
    files = [
        (output_dir / f"{name}_overview.svg", _render_overview(snapshot)),
        (output_dir / f"{name}_gap_distribution.svg", _render_gap_distribution(snapshot)),
        (output_dir / f"{name}_residue_drift.svg", _render_residue_drift(snapshot)),
    ]
    for path, content in files:
        path.write_text(content, encoding="utf-8")
    return [path for path, _ in files]


def write_manifest(snapshots: list[dict[str, Any]], output: str | Path) -> None:
    manifest = {
        "schema": "primeproject.snapshot-manifest.v1",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "snapshots": [
            {
                "label": _label_limit(snapshot["limit"]),
                "slug": f"prime_measure_{_compact_limit(snapshot['limit'])}",
                "limit": snapshot["limit"],
                "modulo": snapshot["modulo"],
                "prime_count": snapshot["prime_count"],
                "max_gap": snapshot["max_gap"],
                "mean_gap": snapshot["mean_gap"],
                "summary_path": f"data/snapshots/prime_measure_{_compact_limit(snapshot['limit'])}.summary.json",
                "overview_svg": f"assets/snapshots/prime_measure_{_compact_limit(snapshot['limit'])}_overview.svg",
                "gap_distribution_svg": f"assets/snapshots/prime_measure_{_compact_limit(snapshot['limit'])}_gap_distribution.svg",
                "residue_drift_svg": f"assets/snapshots/prime_measure_{_compact_limit(snapshot['limit'])}_residue_drift.svg",
            }
            for snapshot in snapshots
        ],
    }
    Path(output).write_text(dumps(manifest, indent=2), encoding="utf-8")


def _render_overview(snapshot: dict[str, Any]) -> str:
    width = 1200
    height = 720
    cards = [
        ("Limit", _label_limit(snapshot["limit"])),
        ("Primes", f"{snapshot['prime_count']:,}"),
        ("Mean gap", f"{snapshot['mean_gap']:.2f}"),
        ("Max gap", f"{snapshot['max_gap']:,}"),
    ]
    card_svg = "\n".join(
        _summary_card(48 + index * 278, 120, label, value)
        for index, (label, value) in enumerate(cards)
    )
    comparison = _comparison_bars(snapshot, 72, 300, 1040, 270)
    tail = "\n".join(
        f"<text x='80' y='{618 + index * 24}' class='small'>{escape(str(item['previous_prime']))} -> {escape(str(item['prime']))}: gap {item['gap']}</text>"
        for index, item in enumerate(snapshot["tail_events"][:3])
    )
    return _svg_document(
        width,
        height,
        f"""
        <text x="48" y="64" class="title">PrimeProject Research Snapshot</text>
        <text x="48" y="92" class="muted">Precomputed local result, rendered as static SVG for GitHub Pages.</text>
        {card_svg}
        <text x="72" y="272" class="section">Generator Comparison</text>
        {comparison}
        <text x="72" y="584" class="section">Largest Tail Events</text>
        {tail}
        """,
    )


def _render_gap_distribution(snapshot: dict[str, Any]) -> str:
    width = 1200
    height = 720
    plot = _line_plot(snapshot, 96, 128, 980, 480)
    return _svg_document(
        width,
        height,
        f"""
        <text x="48" y="64" class="title">Gap Distribution</text>
        <text x="48" y="92" class="muted">Weighted histogram mass by prime gap bin for each observation measure.</text>
        {plot}
        <text x="96" y="650" class="small">teal next_prime | amber rejection | indigo wheel30_next</text>
        """,
    )


def _render_residue_drift(snapshot: dict[str, Any]) -> str:
    width = 1200
    height = 720
    heatmap = _residue_heatmap(snapshot, 108, 150, 960, 300)
    bars = _residue_bar_strip(snapshot, "next_prime", 108, 520, 960, 110)
    return _svg_document(
        width,
        height,
        f"""
        <text x="48" y="64" class="title">Residue Drift</text>
        <text x="48" y="92" class="muted">Deviation from uniform coprime residue mass under generator-induced measures.</text>
        {heatmap}
        {bars}
        """,
    )


def _summary_card(x: int, y: int, label: str, value: str) -> str:
    return f"""
    <rect x="{x}" y="{y}" width="244" height="112" rx="8" class="card"/>
    <text x="{x + 20}" y="{y + 42}" class="muted">{escape(label)}</text>
    <text x="{x + 20}" y="{y + 82}" class="metric">{escape(value)}</text>
    """


def _comparison_bars(snapshot: dict[str, Any], x: int, y: int, width: int, height: int) -> str:
    max_gap = max(item["weighted_mean_gap"] for item in snapshot["generators"].values())
    rows = []
    for index, generator in enumerate(GENERATORS):
        summary = snapshot["generators"][generator]
        row_y = y + 34 + index * 78
        bar_width = (summary["weighted_mean_gap"] / max_gap) * (width - 220)
        rows.append(
            f"""
            <text x="{x}" y="{row_y + 18}" class="label">{generator}</text>
            <rect x="{x + 160}" y="{row_y}" width="{bar_width:.2f}" height="28" fill="{GENERATOR_COLORS[generator]}"/>
            <text x="{x + 170 + bar_width:.2f}" y="{row_y + 20}" class="small">gap {summary['weighted_mean_gap']:.2f} / drift {summary['residue_total_variation']:.4f}</text>
            """
        )
    return f"<g>{''.join(rows)}</g>"


def _line_plot(snapshot: dict[str, Any], x: int, y: int, width: int, height: int) -> str:
    max_mass = max(
        bin_item["mass"]
        for generator in GENERATORS
        for bin_item in snapshot["generators"][generator]["gap_histogram"]
    )
    lines = []
    for generator in GENERATORS:
        histogram = snapshot["generators"][generator]["gap_histogram"]
        points = []
        for index, item in enumerate(histogram):
            px = x + (index / max(1, len(histogram) - 1)) * width
            py = y + height - (item["mass"] / max_mass) * height
            points.append(f"{px:.2f},{py:.2f}")
        lines.append(
            f"<polyline points='{' '.join(points)}' fill='none' stroke='{GENERATOR_COLORS[generator]}' stroke-width='4' stroke-linejoin='round'/>"
        )
    return f"""
    <line x1="{x}" y1="{y + height}" x2="{x + width}" y2="{y + height}" class="axis"/>
    <line x1="{x}" y1="{y}" x2="{x}" y2="{y + height}" class="axis"/>
    {''.join(lines)}
    <text x="{x}" y="{y + height + 42}" class="label">gap bin</text>
    <text x="{x}" y="{y - 18}" class="label">weighted mass</text>
    """


def _residue_heatmap(snapshot: dict[str, Any], x: int, y: int, width: int, height: int) -> str:
    residues = [item["residue"] for item in snapshot["generators"]["next_prime"]["residue_distribution"]]
    step = max(1, len(residues) // 32)
    shown = residues[::step]
    cell_w = width / len(shown)
    cell_h = 58
    rows = []
    for row, generator in enumerate(GENERATORS):
        dist = {item["residue"]: item["mass"] for item in snapshot["generators"][generator]["residue_distribution"]}
        uniform = 1 / len(residues)
        rows.append(f"<text x='{x - 94}' y='{y + row * cell_h + 34}' class='label'>{generator}</text>")
        for col, residue in enumerate(shown):
            delta = dist.get(residue, 0.0) - uniform
            intensity = min(1.0, abs(delta) / uniform)
            color = _mix("#dff4f1" if delta >= 0 else "#fff4df", "#087f7a" if delta >= 0 else "#d78a11", intensity)
            rows.append(
                f"<rect x='{x + col * cell_w:.2f}' y='{y + row * cell_h}' width='{max(1, cell_w - 2):.2f}' height='{cell_h - 8}' fill='{color}'/>"
            )
            if row == len(GENERATORS) - 1 and col % max(1, len(shown) // 12) == 0:
                rows.append(f"<text x='{x + col * cell_w:.2f}' y='{y + height - 32}' class='small'>{residue}</text>")
    return f"<g>{''.join(rows)}</g>"


def _residue_bar_strip(snapshot: dict[str, Any], generator: str, x: int, y: int, width: int, height: int) -> str:
    distribution = snapshot["generators"][generator]["residue_distribution"]
    step = max(1, len(distribution) // 32)
    shown = distribution[::step]
    max_mass = max(item["mass"] for item in shown)
    bar_w = width / len(shown)
    bars = []
    for index, item in enumerate(shown):
        bar_h = (item["mass"] / max_mass) * height
        bars.append(
            f"<rect x='{x + index * bar_w:.2f}' y='{y + height - bar_h:.2f}' width='{max(1, bar_w - 3):.2f}' height='{bar_h:.2f}' fill='#087f7a'/>"
        )
    return f"""
    <text x="{x}" y="{y - 24}" class="section">next_prime residue mass strip</text>
    <line x1="{x}" y1="{y + height}" x2="{x + width}" y2="{y + height}" class="axis"/>
    {''.join(bars)}
    """


def _svg_document(width: int, height: int, body: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
  <style>
    svg {{ background: #ffffff; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    .title {{ fill: #17191f; font-size: 32px; font-weight: 800; }}
    .section {{ fill: #17191f; font-size: 20px; font-weight: 800; }}
    .metric {{ fill: #17191f; font-size: 30px; font-weight: 820; }}
    .label {{ fill: #3a414d; font-size: 14px; font-weight: 700; }}
    .muted {{ fill: #626873; font-size: 15px; font-weight: 600; }}
    .small {{ fill: #626873; font-size: 13px; font-weight: 650; }}
    .card {{ fill: #f4f7fa; stroke: #d9dee7; }}
    .axis {{ stroke: #d9dee7; stroke-width: 2; }}
  </style>
  {body}
</svg>
"""


def _wheel30_count(previous_prime: int, prime: int) -> int:
    count = 0
    for value in range(previous_prime + 1, prime + 1):
        if value % 30 in WHEEL_30_RESIDUES:
            count += 1
    return max(count, 1)


def _compact_limit(limit: int) -> str:
    if limit >= 1_000_000_000 and limit % 1_000_000_000 == 0:
        return f"{limit // 1_000_000_000}b"
    if limit >= 1_000_000 and limit % 1_000_000 == 0:
        return f"{limit // 1_000_000}m"
    if limit >= 1_000 and limit % 1_000 == 0:
        return f"{limit // 1_000}k"
    return str(limit)


def _label_limit(limit: int) -> str:
    if limit >= 1_000_000_000:
        return f"{limit / 1_000_000_000:g}B"
    if limit >= 1_000_000:
        return f"{limit / 1_000_000:g}M"
    if limit >= 1_000:
        return f"{limit / 1_000:g}K"
    return str(limit)


def _mix(start: str, end: str, ratio: float) -> str:
    ratio = max(0.0, min(1.0, ratio))
    start_rgb = _hex_to_rgb(start)
    end_rgb = _hex_to_rgb(end)
    mixed = tuple(round(s + (e - s) * ratio) for s, e in zip(start_rgb, end_rgb))
    return f"#{mixed[0]:02x}{mixed[1]:02x}{mixed[2]:02x}"


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    text = value.removeprefix("#")
    return int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16)

