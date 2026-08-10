import unittest

from src.source_checker import (
    check_source,
    normalize_status,
)


class TestSourceChecker(unittest.TestCase):

    def test_romano_here_we_go(self):
        result = check_source(
            "Fabrizio Romano",
            "here we go",
        )

        self.assertEqual(result.confidence, 90)
        self.assertEqual(
            result.verdict,
            "VERY HIGH CONFIDENCE",
        )

    def test_bbc_reported(self):
        result = check_source(
            "BBC Sport",
            "reported",
        )

        self.assertEqual(result.source_score, 90)
        self.assertEqual(result.status_score, 70)
        self.assertEqual(result.confidence, 83)
        self.assertEqual(
            result.verdict,
            "HIGH CONFIDENCE",
        )

    def test_official_source(self):
        result = check_source(
            "Liverpool FC Official",
            "official",
        )

        self.assertEqual(result.source_score, 100)
        self.assertEqual(result.status_score, 100)
        self.assertEqual(result.confidence, 100)
        self.assertEqual(
            result.verdict,
            "OFFICIAL",
        )

    def test_unrated_rumour(self):
        result = check_source(
            "Random Twitter Account",
            "rumour",
        )

        self.assertEqual(result.source_score, 40)
        self.assertEqual(result.status_score, 40)
        self.assertEqual(result.confidence, 40)
        self.assertEqual(
            result.verdict,
            "LOW CONFIDENCE",
        )

    def test_rumor_alias(self):
        result = check_source(
            "Unknown Source",
            "rumor",
        )

        self.assertEqual(
            result.status,
            "rumour",
        )

    def test_score_components_are_exposed(self):
        result = check_source(
            "BBC Sport",
            "reported",
        )

        self.assertEqual(result.source_score, 90)
        self.assertEqual(result.status_score, 70)

    def test_invalid_status(self):
        with self.assertRaises(ValueError):
            normalize_status("breaking")


if __name__ == "__main__":
    unittest.main()
