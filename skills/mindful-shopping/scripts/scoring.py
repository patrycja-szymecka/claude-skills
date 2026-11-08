"""Manipulation-risk scoring.

This module is the source of truth for every number on the dashboard. The formulas are
documented in references/scoring.md; the HTML template only falls back to its own copy of
them when an analysis was built without this script.
"""

import math
from dataclasses import asdict, dataclass, field
from typing import Any

# Base weights from references/biases.md. Keeping them here lets validation flag a weight
# that drifted from the catalog, which would make analyses incomparable.
CATALOG_WEIGHTS: dict[str, float] = {
    "anchoring": 1.3,
    "framing": 1.0,
    "decoy": 1.0,
    "zero_price": 1.0,
    "bundling": 0.8,
    "drip_pricing": 1.0,
    "price_quality": 0.7,
    "urgency_fomo": 1.3,
    "scarcity": 1.2,
    "loss_aversion": 1.1,
    "social_proof": 1.0,
    "authority": 0.8,
    "reciprocity": 0.7,
    "default_effect": 0.9,
    "commitment": 0.9,
    "endowment": 0.8,
    "pain_of_paying": 1.2,
    "present_bias": 0.9,
    "mental_accounting": 0.8,
    "emotional_spending": 1.0,
    "confirmation_bias": 0.8,
    "halo": 0.7,
}

TACTICS_SATURATION = 12.0
WEIGHT_TACTICS = 0.45
WEIGHT_PRICE = 0.30
WEIGHT_VULNERABILITY = 0.25

FAKE_DISCOUNT_FACTOR = 2.5
PROMO_FREQUENCY_FACTOR = 6.0
ABOVE_COMPETITION_FACTOR = 4.0
ABOVE_HISTORICAL_LOW_FACTOR = 3.0

SAME_PRODUCT = "ten sam produkt"

ZONES: tuple[tuple[float, str, str], ...] = (
    (25, "good", "Niski"),
    (50, "warning", "Umiarkowany"),
    (75, "serious", "Wysoki"),
    (math.inf, "critical", "Bardzo wysoki"),
)


@dataclass(frozen=True, slots=True)
class BiasScore:
    id: str
    name: str
    raw: float
    share: float


@dataclass(frozen=True, slots=True)
class PricePart:
    name: str
    value: float


@dataclass(frozen=True, slots=True)
class Zone:
    key: str
    label: str


@dataclass(frozen=True, slots=True)
class Scores:
    index: float
    zone: Zone
    tactics: float
    price_risk: float | None
    vulnerability: float | None
    weights: dict[str, float]
    price_parts: list[PricePart] = field(default_factory=list)
    biases: list[BiasScore] = field(default_factory=list)
    claimed_discount_pct: float | None = None
    real_discount_pct: float | None = None
    reference_price: float | None = None
    best_alternative_price: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def as_number(value: object) -> float | None:
    """Return value as float when it is a real number (bools and NaN don't count)."""
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return float(value) if math.isfinite(value) else None


def number_or(value: object, default: float) -> float:
    number = as_number(value)
    return default if number is None else number


def zone_of(index: float) -> Zone:
    for upper, key, label in ZONES:
        if index < upper:
            return Zone(key, label)
    raise AssertionError("unreachable: the last zone is unbounded")


def score_biases(biases: list[dict[str, Any]]) -> tuple[list[BiasScore], float]:
    """Return per-bias shares (sorted, largest first) and the tactics score."""
    raws: list[tuple[dict[str, Any], float]] = []
    tactic_sum = 0.0
    for bias in biases:
        weight = number_or(bias.get("weight"), 1.0)
        intensity = clamp(number_or(bias.get("intensity"), 0.0), 0, 3)
        amplifier = clamp(number_or(bias.get("amplifier"), 1.0), 0.5, 2)
        raws.append((bias, weight * intensity * amplifier))
        if bias.get("source") != "context":
            tactic_sum += weight * intensity

    total = sum(raw for _, raw in raws)
    scored = [
        BiasScore(
            id=str(bias.get("id", "")),
            name=str(bias.get("name", "")),
            raw=round(raw, 4),
            share=round(raw / total * 100, 2) if total else 0.0,
        )
        for bias, raw in raws
    ]
    scored.sort(key=lambda b: b.share, reverse=True)
    tactics = 100 * (1 - math.exp(-tactic_sum / TACTICS_SATURATION))
    return scored, tactics


def score_price(data: dict[str, Any]) -> tuple[float | None, list[PricePart], dict[str, Any]]:
    """Return the price-integrity risk, its parts, and the discount facts behind it."""
    offer = data.get("offer") or {}
    price = data.get("price") or {}
    current = as_number(offer.get("current_price"))
    reference = as_number(offer.get("lowest_30d_price")) or as_number(price.get("typical_price"))

    real_discount = (
        (reference - current) / reference * 100 if current is not None and reference else None
    )

    claimed = as_number(offer.get("claimed_discount_pct"))
    old_price = as_number(offer.get("claimed_old_price"))
    if claimed is None and old_price and current is not None:
        claimed = (old_price - current) / old_price * 100

    parts: list[PricePart] = []
    if claimed is not None and real_discount is not None:
        parts.append(
            PricePart("Fałszywy rabat", clamp((claimed - real_discount) * FAKE_DISCOUNT_FACTOR))
        )

    promos = as_number(price.get("promos_per_year"))
    if promos is not None:
        parts.append(PricePart("Wieczna promocja", clamp(promos * PROMO_FREQUENCY_FACTOR)))

    same_product = [
        p
        for alt in data.get("alternatives") or []
        if alt.get("type") == SAME_PRODUCT and (p := as_number(alt.get("price"))) is not None
    ]
    best_alternative = min(same_product) if same_product else None
    if best_alternative and current is not None:
        above = (current - best_alternative) / best_alternative * 100
        parts.append(PricePart("Drożej niż konkurencja", clamp(above * ABOVE_COMPETITION_FACTOR)))

    low = as_number(price.get("historical_low"))
    if low and current is not None:
        above_low = (current - low) / low * 100
        parts.append(
            PricePart(
                "Drożej niż minimum historyczne", clamp(above_low * ABOVE_HISTORICAL_LOW_FACTOR)
            )
        )

    risk = sum(p.value for p in parts) / len(parts) if parts else None
    facts = {
        "claimed_discount_pct": claimed,
        "real_discount_pct": real_discount,
        "reference_price": reference,
        "best_alternative_price": best_alternative,
    }
    return risk, parts, facts


def score_vulnerability(survey: list[dict[str, Any]]) -> float | None:
    risks = [clamp(r, 0, 1) for s in survey if (r := as_number(s.get("risk"))) is not None]
    return sum(risks) / len(risks) * 100 if risks else None


def compute_scores(data: dict[str, Any]) -> Scores:
    biases, tactics = score_biases(data.get("biases") or [])
    price_risk, price_parts, facts = score_price(data)
    vulnerability = score_vulnerability(data.get("survey") or [])

    w_tactics = WEIGHT_TACTICS
    w_price = WEIGHT_PRICE if price_risk is not None else 0.0
    w_vuln = WEIGHT_VULNERABILITY if vulnerability is not None else 0.0
    total_weight = w_tactics + w_price + w_vuln
    index = (
        w_tactics * tactics + w_price * (price_risk or 0.0) + w_vuln * (vulnerability or 0.0)
    ) / total_weight

    def r(value: float | None, digits: int = 2) -> float | None:
        return None if value is None else round(value, digits)

    return Scores(
        index=round(index, 2),
        zone=zone_of(index),
        tactics=round(tactics, 2),
        price_risk=r(price_risk),
        vulnerability=r(vulnerability),
        weights={
            "tactics": round(w_tactics / total_weight, 4),
            "price": round(w_price / total_weight, 4),
            "vulnerability": round(w_vuln / total_weight, 4),
        },
        price_parts=[PricePart(p.name, round(p.value, 2)) for p in price_parts],
        biases=biases,
        claimed_discount_pct=r(facts["claimed_discount_pct"]),
        real_discount_pct=r(facts["real_discount_pct"]),
        reference_price=r(facts["reference_price"]),
        best_alternative_price=r(facts["best_alternative_price"]),
    )
