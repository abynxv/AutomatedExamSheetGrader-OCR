import unittest
import pandas as pd
from src.grader import grade_student


class TestGrader(unittest.TestCase):

    def setUp(self):
        self.answer_key = pd.DataFrame([
            {'question_id': 1, 'correct_answer': 'A', 'points': 2},
            {'question_id': 2, 'correct_answer': 'B', 'points': 3},
            {'question_id': 3, 'correct_answer': 'Photosynthesis', 'points': 5}
        ])

    def test_all_correct(self):
        answers = {'1': 'a', '2': 'b', '3': 'photosynthesis'}
        score, _ = grade_student(answers, self.answer_key)
        self.assertEqual(score, 10)

    def test_partial_correct(self):
        answers = {'1': 'a', '2': 'x'}
        score, _ = grade_student(answers, self.answer_key)
        self.assertEqual(score, 2)

    def test_all_wrong(self):
        answers = {'1': 'x', '2': 'y', '3': 'z'}
        score, _ = grade_student(answers, self.answer_key)
        self.assertEqual(score, 0)
