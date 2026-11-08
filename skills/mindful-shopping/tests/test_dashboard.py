import copy
import json
import unittest
from pathlib import Path

from build_dashboard import PLACEHOLDER, TEMPLATE, build_html, embed, slugify
from scoring import compute_scores, zone_of
from validation import validate

SAMPLE = Path(__file__).resolve().parent.parent / "assets" / "sample_analysis.json"


def sample() -> dict:
    return json.loads(SAMPLE.read_text(encoding="utf-8"))


class ScoringTest(unittest.TestCase):
    def test_sample_scores(self) -> None:
        scores = compute_scores(sample())
        self.assertAlmostEqual(scores.index, 67.63, places=2)
        self.assertEqual(scores.vulnerability, 62.5)
        self.assertEqual(scores.zone.label, "Wysoki")
        self.assertAlmostEqual(scores.real_discount_pct or 0, 3.71, places=2)
        self.assertEqual(scores.best_alternative_price, 1049)

    def test_shares_sum_to_100_and_are_sorted(self) -> None:
        shares = [b.share for b in compute_scores(sample()).biases]
        self.assertAlmostEqual(sum(shares), 100, delta=0.05)
        self.assertEqual(shares, sorted(shares, reverse=True))

    def test_context_biases_do_not_count_as_tactics(self) -> None:
        data = sample()
        only_context = copy.deepcopy(data)
        for bias in only_context["biases"]:
            bias["source"] = "context"
        self.assertEqual(compute_scores(only_context).tactics, 0)

    def test_missing_price_data_reweights_index(self) -> None:
        data = sample()
        data["price"] = {}
        data["alternatives"] = []
        for key in ("claimed_discount_pct", "claimed_old_price", "lowest_30d_price"):
            data["offer"].pop(key)
        scores = compute_scores(data)
        self.assertIsNone(scores.price_risk)
        self.assertAlmostEqual(sum(scores.weights.values()), 1, places=3)
        self.assertEqual(scores.weights["price"], 0)

    def test_zone_boundaries(self) -> None:
        self.assertEqual(zone_of(24.9).key, "good")
        self.assertEqual(zone_of(25).key, "warning")
        self.assertEqual(zone_of(75).key, "critical")


class ValidationTest(unittest.TestCase):
    def test_sample_is_valid(self) -> None:
        report = validate(sample())
        self.assertEqual(report.errors, [])

    def test_rejects_bad_values(self) -> None:
        data = sample()
        data["biases"][0]["intensity"] = 5
        data["biases"][1]["source"] = "ad"
        data["survey"][0]["risk"] = "high"
        data["verdict"]["decision"] = "maybe"
        errors = " ".join(validate(data).errors)
        for fragment in ("intensity", "source", "risk", "decision"):
            self.assertIn(fragment, errors)

    def test_bool_is_not_a_number(self) -> None:
        data = sample()
        data["offer"]["current_price"] = True
        self.assertFalse(validate(data).ok)

    def test_warns_about_weight_drift(self) -> None:
        data = sample()
        data["biases"][0]["weight"] = 2.0
        self.assertTrue(any("katalogu" in w for w in validate(data).warnings))


class BuildTest(unittest.TestCase):
    def test_embeds_data_and_scores(self) -> None:
        data = sample()
        data["offer"]["title"] = "Test </script><b>x</b>"
        html, scores = build_html(data, TEMPLATE.read_text(encoding="utf-8"))
        self.assertNotIn(PLACEHOLDER, html)
        self.assertNotIn("</script><b>", html)
        self.assertIn('"scores"', html)
        self.assertIn(f'"index": {scores.index}', html)

    def test_template_needs_exactly_one_placeholder(self) -> None:
        with self.assertRaises(ValueError):
            embed("<html></html>", {})

    def test_slugify_polish(self) -> None:
        self.assertEqual(slugify("Słuchawki Żółte ĄĘ (przykład)"), "sluchawki-zolte-ae-przyklad")


if __name__ == "__main__":
    unittest.main()
