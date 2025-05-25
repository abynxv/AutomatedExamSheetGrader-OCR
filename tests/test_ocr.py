import unittest
import numpy as np
import cv2
from src.ocr import extract_text


class TestOCR(unittest.TestCase):

    def create_test_image(self, text):
        img = np.ones((100, 400), dtype=np.uint8) * 255
        cv2.putText(img, text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,), 2, cv2.LINE_AA)
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    def test_extract_text(self):
        img = self.create_test_image("Hello OCR")
        result = extract_text(img).lower()
        self.assertIn("hello", result)

    def test_extract_empty(self):
        img = np.ones((100, 400, 3), dtype=np.uint8) * 255
        result = extract_text(img)
        self.assertEqual(result.strip(), "")

