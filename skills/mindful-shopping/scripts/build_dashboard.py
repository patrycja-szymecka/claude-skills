"""Build the mindful-shopping dashboard from an analysis JSON file.

Usage (from anywhere):
    uv run --project <skill-dir> <skill-dir>/scripts/build_dashboard.py analysis.json [-o out.html]

Validates the data, computes all scores (scoring.py), embeds data + scores into
assets/dashboard_template.html, writes the HTML and prints a summary for the chat.

Exit codes: 0 built, 1 validation errors, 2 input/output problem.
"""

import argparse
import io
import json
import math
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

from scoring import Scores, compute_scores
from validation import Report, validate

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "dashboard_template.html"
PLACEHOLDER = "/*__ANALYSIS_DATA__*/null"


def slugify(text: str, max_length: int = 60) -> str:
    text = text.replace("ł", "l").replace("Ł", "L")
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug[:max_length].rstrip("-") or "oferta"


def default_output(data: dict[str, Any]) -> Path:
    date = (data.get("meta") or {}).get("generated_at", "analiza")
    title = (data.get("offer") or {}).get("title", "oferta")
    return Path.cwd() / "analizy" / f"{date}-{slugify(str(title))}.html"


def embed(template: str, payload: dict[str, Any]) -> str:
    if template.count(PLACEHOLDER) != 1:
        raise ValueError(f"Szablon musi zawierać dokładnie jeden znacznik {PLACEHOLDER}")
    # "</" inside a string would close the <script> element early.
    data_js = json.dumps(payload, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return template.replace(PLACEHOLDER, data_js)


def build_html(data: dict[str, Any], template: str) -> tuple[str, Scores]:
    scores = compute_scores(data)
    payload = {**data, "scores": scores.to_dict()}
    return embed(template, payload), scores


def _pct(value: float | None, digits: int = 0) -> str:
    """Format like the dashboard does: round half up (Python's round() is half-to-even)."""
    if value is None:
        return "brak danych"
    scale = 10**digits
    return f"{math.floor(value * scale + 0.5) / scale:.{digits}f}%"


def summary_text(scores: Scores, report: Report, output: Path | None) -> str:
    lines = [
        f"Wskaźnik ryzyka manipulacji: {_pct(scores.index)} ({scores.zone.label})",
        f"  Taktyki {_pct(scores.tactics)} · Nierzetelność ceny {_pct(scores.price_risk)}"
        f" · Podatność {_pct(scores.vulnerability)}",
        f"Rabat deklarowany {_pct(scores.claimed_discount_pct, 1)}"
        f" · realny {_pct(scores.real_discount_pct, 1)}",
        "Najsilniejsze efekty:",
    ]
    lines += [f"  {i}. {b.name} — {_pct(b.share)}" for i, b in enumerate(scores.biases[:3], 1)]
    if report.warnings:
        lines.append(f"Ostrzeżenia ({len(report.warnings)}):")
        lines += [f"  - {w}" for w in report.warnings]
    if output:
        lines.append(f"Zapisano: {output}")
    return "\n".join(lines)


def load_json(source: str) -> Any:
    if source == "-":
        return json.load(sys.stdin)
    return json.loads(Path(source).read_text(encoding="utf-8-sig"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("input", help="plik JSON z analizą (lub '-' dla stdin)")
    parser.add_argument("-o", "--output", type=Path, help="ścieżka pliku HTML")
    parser.add_argument("--check", action="store_true", help="tylko walidacja i wyniki, bez HTML")
    parser.add_argument("--json", action="store_true", help="wypisz wyniki jako JSON")
    args = parser.parse_args(argv)

    # Polish text must survive legacy Windows consoles too.
    for stream in (sys.stdout, sys.stderr):
        if isinstance(stream, io.TextIOWrapper):
            stream.reconfigure(encoding="utf-8")

    try:
        data = load_json(args.input)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Nie można wczytać danych: {exc}", file=sys.stderr)
        return 2

    report = validate(data)
    if not report.ok:
        print(f"Błędy w danych ({len(report.errors)}):", file=sys.stderr)
        for error in report.errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    output: Path | None = None
    if args.check:
        scores = compute_scores(data)
    else:
        try:
            html, scores = build_html(data, TEMPLATE.read_text(encoding="utf-8"))
            output = (args.output or default_output(data)).resolve()
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(html, encoding="utf-8")
        except (OSError, ValueError) as exc:
            print(f"Nie można zbudować dashboardu: {exc}", file=sys.stderr)
            return 2

    if args.json:
        result = {
            "output": str(output) if output else None,
            "warnings": report.warnings,
            "scores": scores.to_dict(),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(summary_text(scores, report, output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
