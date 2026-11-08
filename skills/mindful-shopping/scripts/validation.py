"""Validation of the analysis JSON described in references/data-schema.md.

Errors stop the build (the dashboard would be wrong or broken); warnings are printed so Claude
can fix them, but the dashboard is still built.
"""

import datetime as dt
from dataclasses import dataclass, field
from typing import Any

from scoring import CATALOG_WEIGHTS, SAME_PRODUCT, as_number

BIAS_SOURCES = {"offer", "context", "both"}
DECISIONS = {"kup", "kup gdzie indziej", "poczekaj", "odpuść"}
CONFIDENCE = {"wysoka", "średnia", "niska"}
ALTERNATIVE_TYPES = {SAME_PRODUCT, "podobny produkt"}


@dataclass(slots=True)
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _is_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _is_url(value: object) -> bool:
    return isinstance(value, str) and value.startswith(("http://", "https://"))


def _str_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(v, str) for v in value)


def _check_number(
    report: Report,
    where: str,
    value: object,
    *,
    required: bool = False,
    low: float | None = None,
    high: float | None = None,
) -> None:
    if value is None:
        if required:
            report.errors.append(f"{where}: pole wymagane (liczba)")
        return
    number = as_number(value)
    if number is None:
        report.errors.append(f"{where}: oczekiwano liczby, jest {value!r}")
    elif (low is not None and number < low) or (high is not None and number > high):
        report.errors.append(f"{where}: {number} poza zakresem {low}–{high}")


def _check_url(report: Report, where: str, value: object) -> None:
    if value not in (None, "") and not _is_url(value):
        report.warnings.append(f"{where}: link nie zaczyna się od http(s):// — zostanie pominięty")


def _section(report: Report, data: dict[str, Any], key: str, kind: type) -> Any:
    value = data.get(key)
    if value is None:
        return kind()
    if not isinstance(value, kind):
        report.errors.append(f"{key}: oczekiwano {'obiektu' if kind is dict else 'listy'}")
        return kind()
    return value


def _validate_meta(report: Report, meta: dict[str, Any]) -> None:
    if not _is_date(meta.get("generated_at")):
        report.errors.append("meta.generated_at: wymagana data RRRR-MM-DD")
    currency = meta.get("currency", "PLN")
    if not (isinstance(currency, str) and len(currency) == 3 and currency.isupper()):
        report.errors.append(f"meta.currency: oczekiwano kodu ISO (np. PLN), jest {currency!r}")
    confidence = str(meta.get("confidence", "")).lower()
    if confidence not in CONFIDENCE:
        report.warnings.append(f"meta.confidence: oczekiwano jednej z {sorted(CONFIDENCE)}")


def _validate_offer(report: Report, offer: dict[str, Any]) -> None:
    if not isinstance(offer.get("title"), str) or not offer["title"].strip():
        report.errors.append("offer.title: wymagany tekst")
    _check_number(report, "offer.current_price", offer.get("current_price"), required=True, low=0)
    _check_number(report, "offer.claimed_old_price", offer.get("claimed_old_price"), low=0)
    _check_number(
        report, "offer.claimed_discount_pct", offer.get("claimed_discount_pct"), low=0, high=100
    )
    _check_number(report, "offer.lowest_30d_price", offer.get("lowest_30d_price"), low=0)
    _check_url(report, "offer.url", offer.get("url"))
    if offer.get("captured_at") is not None and not _is_date(offer["captured_at"]):
        report.errors.append("offer.captured_at: oczekiwano daty RRRR-MM-DD")
    if "key_specs" in offer and not _str_list(offer["key_specs"]):
        report.errors.append("offer.key_specs: oczekiwano listy tekstów")


def _validate_survey(report: Report, survey: list[Any]) -> None:
    if not survey:
        report.warnings.append(
            "survey: brak odpowiedzi — wskaźnik podatności nie zostanie policzony"
        )
    for i, item in enumerate(survey):
        where = f"survey[{i}]"
        if not isinstance(item, dict):
            report.errors.append(f"{where}: oczekiwano obiektu")
            continue
        for key in ("question", "answer"):
            if not isinstance(item.get(key), str):
                report.errors.append(f"{where}.{key}: wymagany tekst")
        _check_number(report, f"{where}.risk", item.get("risk"), required=True, low=0, high=1)


def _validate_biases(report: Report, biases: list[Any]) -> None:
    if not biases:
        report.errors.append("biases: lista nie może być pusta")
    seen: set[str] = set()
    for i, bias in enumerate(biases):
        where = f"biases[{i}]"
        if not isinstance(bias, dict):
            report.errors.append(f"{where}: oczekiwano obiektu")
            continue
        bias_id = bias.get("id")
        if not isinstance(bias_id, str) or not bias_id:
            report.errors.append(f"{where}.id: wymagany identyfikator z katalogu")
        elif bias_id in seen:
            report.errors.append(f"{where}.id: powtórzony identyfikator {bias_id!r}")
        else:
            seen.add(bias_id)
            where = f"biases[{bias_id}]"
        if not isinstance(bias.get("name"), str) or not bias["name"]:
            report.errors.append(f"{where}.name: wymagany tekst")

        _check_number(report, f"{where}.weight", bias.get("weight"), required=True, low=0.1, high=3)
        _check_number(
            report, f"{where}.intensity", bias.get("intensity"), required=True, low=0, high=3
        )
        _check_number(report, f"{where}.amplifier", bias.get("amplifier"), low=0.5, high=2)

        amplifier = as_number(bias.get("amplifier"))
        if amplifier is not None and not 0.8 <= amplifier <= 1.5:
            report.warnings.append(
                f"{where}.amplifier: {amplifier} poza zalecanym zakresem 0.8–1.5"
            )
        catalog_weight = CATALOG_WEIGHTS.get(str(bias_id))
        weight = as_number(bias.get("weight"))
        if catalog_weight is None:
            report.warnings.append(f"{where}: efekt spoza katalogu references/biases.md")
        elif weight is not None and weight != catalog_weight:
            report.warnings.append(
                f"{where}.weight: {weight} różni się od wagi z katalogu ({catalog_weight})"
            )

        source = bias.get("source")
        if source not in BIAS_SOURCES:
            report.errors.append(f"{where}.source: oczekiwano jednej z {sorted(BIAS_SOURCES)}")
        for key in ("evidence", "defense"):
            if key in bias and not _str_list(bias[key]):
                report.errors.append(f"{where}.{key}: oczekiwano listy tekstów")
        if source in {"offer", "both"} and not bias.get("evidence"):
            report.warnings.append(f"{where}: źródło {source!r} bez dowodów ze strony (evidence)")
        if not bias.get("defense"):
            report.warnings.append(f"{where}: brak rad, jak się nie dać (defense)")


def _validate_price(report: Report, price: dict[str, Any]) -> None:
    history = price.get("history") or []
    if not isinstance(history, list):
        report.errors.append("price.history: oczekiwano listy")
        history = []
    for i, point in enumerate(history):
        where = f"price.history[{i}]"
        if not isinstance(point, dict):
            report.errors.append(f"{where}: oczekiwano obiektu")
            continue
        if not _is_date(point.get("date")):
            report.errors.append(f"{where}.date: oczekiwano daty RRRR-MM-DD")
        _check_number(report, f"{where}.price", point.get("price"), required=True, low=0)
    if len(history) < 2:
        report.warnings.append("price.history: mniej niż 2 punkty — wykres nie zostanie narysowany")
    for key in ("historical_low", "typical_price", "promos_per_year"):
        _check_number(report, f"price.{key}", price.get(key), low=0)
    if price.get("historical_low_date") is not None and not _is_date(price["historical_low_date"]):
        report.errors.append("price.historical_low_date: oczekiwano daty RRRR-MM-DD")
    for i, src in enumerate(price.get("sources") or []):
        _check_url(
            report, f"price.sources[{i}].url", src.get("url") if isinstance(src, dict) else None
        )


def _validate_alternatives(report: Report, alternatives: list[Any]) -> None:
    if not alternatives:
        report.warnings.append("alternatives: brak alternatyw do porównania")
    for i, alt in enumerate(alternatives):
        where = f"alternatives[{i}]"
        if not isinstance(alt, dict):
            report.errors.append(f"{where}: oczekiwano obiektu")
            continue
        if not isinstance(alt.get("name"), str) or not alt["name"]:
            report.errors.append(f"{where}.name: wymagany tekst")
        _check_number(report, f"{where}.price", alt.get("price"), low=0)
        if alt.get("type") not in ALTERNATIVE_TYPES:
            report.errors.append(f"{where}.type: oczekiwano jednej z {sorted(ALTERNATIVE_TYPES)}")
        _check_url(report, f"{where}.url", alt.get("url"))


def _validate_verdict(report: Report, verdict: dict[str, Any]) -> None:
    decision = str(verdict.get("decision", "")).lower()
    if decision not in DECISIONS:
        report.errors.append(f"verdict.decision: oczekiwano jednej z {sorted(DECISIONS)}")
    if not verdict.get("headline"):
        report.warnings.append("verdict.headline: brak jednozdaniowego werdyktu")
    if "reasons" in verdict and not _str_list(verdict["reasons"]):
        report.errors.append("verdict.reasons: oczekiwano listy tekstów")
    _check_number(report, "verdict.target_price", verdict.get("target_price"), low=0)


def validate(data: object) -> Report:
    report = Report()
    if not isinstance(data, dict):
        report.errors.append("Dane muszą być obiektem JSON")
        return report

    if "scores" in data:
        report.warnings.append("scores: pole zostanie nadpisane wynikami policzonymi przez skrypt")

    _validate_meta(report, _section(report, data, "meta", dict))
    _validate_offer(report, _section(report, data, "offer", dict))
    _validate_survey(report, _section(report, data, "survey", list))
    _validate_biases(report, _section(report, data, "biases", list))
    _validate_price(report, _section(report, data, "price", dict))
    _validate_alternatives(report, _section(report, data, "alternatives", list))
    _validate_verdict(report, _section(report, data, "verdict", dict))

    for key in ("checklist", "limitations"):
        if not _str_list(_section(report, data, key, list)):
            report.errors.append(f"{key}: oczekiwano listy tekstów")
    for i, src in enumerate(_section(report, data, "sources", list)):
        _check_url(report, f"sources[{i}].url", src.get("url") if isinstance(src, dict) else None)
    return report
