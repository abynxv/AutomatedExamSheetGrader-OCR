import unittest
import numpy as np
import cv2
from src.preprocessor import deskew, correct_orientation, enhance_image


class TestImagePreprocessing(unittest.TestCase):

    def setUp(self):
        self.blank = np.ones((100, 400, 3), dtype=np.uint8) * 255
        self.text_img = self.blank.copy()
        cv2.putText(self.text_img, "Test", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)

    def test_deskew_returns_same_shape(self):
        result = deskew(self.text_img)
        self.assertEqual(result.shape, self.text_img.shape)

    def test_correct_orientation_no_change(self):
        result = correct_orientation(self.text_img)
        self.assertTrue(np.array_equal(result, self.text_img))  # Placeholder until logic added

    def test_enhance_image_output(self):
        result = enhance_image(self.text_img)
        self.assertEqual(result.shape, self.text_img.shape)
        self.assertTrue(np.max(result) <= 255 and np.min(result) >= 0)
