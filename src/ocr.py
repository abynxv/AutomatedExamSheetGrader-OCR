import pytesseract
from PIL import Image
import cv2
import numpy as np
import os

def extract_text(image, debug=False, debug_dir="debug", filename="image"):
    if debug and not os.path.exists(debug_dir):
        os.makedirs(debug_dir)

    # Step 1: Convert to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if debug:
        cv2.imwrite(os.path.join(debug_dir, f"{filename}_1_gray.png"), gray)

    # Step 2: Thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if debug:
        cv2.imwrite(os.path.join(debug_dir, f"{filename}_2_thresh.png"), thresh)

    # Step 3: Noise Removal
    kernel = np.ones((1, 1), np.uint8)
    clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    if debug:
        cv2.imwrite(os.path.join(debug_dir, f"{filename}_3_clean.png"), clean)

    # Step 4: Try Multiple Variants
    ocr_texts = []
    configs = [r'--oem 3 --psm 6', r'--oem 3 --psm 4', r'--oem 3 --psm 11']
    images_to_try = [clean, thresh, gray]

    for config in configs:
        for img in images_to_try:
            pil_img = Image.fromarray(img)
            text = pytesseract.image_to_string(pil_img, lang='eng', config=config).strip()
            if text:
                return text  # Return on first non-empty result
            ocr_texts.append((config, text))

    # If all failed, return best-effort result (likely empty)
    if debug:
        with open(os.path.join(debug_dir, f"{filename}_ocr_attempts.txt"), 'w') as f:
            for config, txt in ocr_texts:
                f.write(f"[Config: {config}]\n{text}\n\n")

    return ""  # or max(ocr_texts, key=lambda x: len(x[1]))[1]
