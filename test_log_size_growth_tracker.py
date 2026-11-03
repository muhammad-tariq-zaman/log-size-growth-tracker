import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import forecast


def row(f, d, size):
    return {"file": f, "date": d, "size_mb": str(size)}


class TestGrowthTracker(unittest.TestCase):
    def test_growth_rate(self):
        result = forecast([row("a.log", "2026-11-01", 100),
                           row("a.log", "2026-11-11", 200)], 1000)
        self.assertAlmostEqual(result[0][1], 10.0)

    def test_over_limit(self):
        result = forecast([row("a.log", "2026-11-01", 1200)], 1000)
        self.assertEqual(result[0][2], "OVER LIMIT")

    def test_shrinking(self):
        result = forecast([row("a.log", "2026-11-01", 200),
                           row("a.log", "2026-11-11", 100)], 1000)
        self.assertEqual(result[0][2], "NOT GROWING")

    def test_eta_date(self):
        result = forecast([row("a.log", "2026-11-01", 0),
                           row("a.log", "2026-11-11", 100)], 200)
        self.assertIn("2026-11-21", result[0][2])
