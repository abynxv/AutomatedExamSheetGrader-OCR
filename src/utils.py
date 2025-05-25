import json
from datetime import datetime
import numpy as np


def compute_statistics(results, total_possible):
    if not results:
        return {
            "average_score": 0.0,
            "median_score": 0.0,
            "highest_score": 0.0,
            "lowest_score": 0.0,
            "standard_deviation": 0.0,
            "grade_distribution": {
                "A (90-100)": 0,
                "B (80-89)": 0,
                "C (70-79)": 0,
                "D (60-69)": 0,
                "F (0-59)": 0
            }
        }

    percentages = [res["percentage"] for res in results]
    return {
        "average_score": round(np.mean(percentages), 2),
        "median_score": round(np.median(percentages), 2),
        "highest_score": round(np.max(percentages), 2),
        "lowest_score": round(np.min(percentages), 2),
        "standard_deviation": round(np.std(percentages), 2),
        "grade_distribution": {
            "A (90-100)": sum(90 <= p <= 100 for p in percentages),
            "B (80-89)": sum(80 <= p < 90 for p in percentages),
            "C (70-79)": sum(70 <= p < 80 for p in percentages),
            "D (60-69)": sum(60 <= p < 70 for p in percentages),
            "F (0-59)": sum(p < 60 for p in percentages),
        }
    }

def save_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
