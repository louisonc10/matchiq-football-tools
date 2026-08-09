import unittest

from src.source_checker import load_source_scores


class TestSourceConfig(unittest.TestCase):

    def setUp(self):
        self.sources = load_source_scores()

    def test_config_is_not_empty(self):
        self.assertTrue(
            len(self.sources) > 0
        )

    def test_source_names_are_valid(self):
        for name in self.sources:
            self.assertIsInstance(
                name,
                str,
            )

            self.assertTrue(
                name.strip()
            )

    def test_scores_are_valid(self):
        for name, data in self.sources.items():
            self.assertIn(
                "score",
                data,
                msg=f"{name} is missing score",
            )

            score = data["score"]

            self.assertIsInstance(
                score,
                int,
                msg=f"{name} score must be an integer",
            )

            self.assertGreaterEqual(
                score,
                0,
                msg=f"{name} score cannot be below 0",
            )

            self.assertLessEqual(
                score,
                100,
                msg=f"{name} score cannot exceed 100",
            )

    def test_tiers_are_valid(self):
        for name, data in self.sources.items():
            self.assertIn(
                "tier",
                data,
                msg=f"{name} is missing tier",
            )

            tier = data["tier"]

            self.assertIsInstance(
                tier,
                str,
                msg=f"{name} tier must be text",
            )

            self.assertTrue(
                tier.strip(),
                msg=f"{name} tier cannot be empty",
            )


if __name__ == "__main__":
    unittest.main()
