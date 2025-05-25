import unittest
import os
import json
from src.utils import compute_statistics, save_json


class TestUtilities(unittest.TestCase):

    def test_compute_statistics_valid(self):
        results = [
            {"percentage": 95},
            {"percentage": 88},
            {"percentage": 72},
            {"percentage": 67},
            {"percentage": 50},
        ]
        stats = compute_statistics(results, 100)
        self.assertEqual(stats["grade_distribution"]["A (90-100)"], 1)
        self.assertEqual(stats["grade_distribution"]["F (0-59)"], 1)

    def test_compute_statistics_empty(self):
        stats = compute_statistics([], 100)
        self.assertEqual(stats["average_score"], 0.0)
        self.assertEqual(stats["grade_distribution"]["F (0-59)"], 0)

    def test_save_json_creates_file(self):
        data = {"test": 123}
        path = "temp_test.json"
        save_json(data, path)
        self.assertTrue(os.path.exists(path))
        with open(path) as f:
            content = json.load(f)
        self.assertEqual(content, data)
        os.remove(path)

