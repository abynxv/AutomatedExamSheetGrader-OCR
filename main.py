import argparse
import os
import cv2
import re
from datetime import datetime
from src import preprocessor, ocr, grader, utils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', required=True)
    parser.add_argument('--key', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--log_file', default='process.log')
    args = parser.parse_args()

    answer_key = grader.load_answer_key(args.key)
    total_possible = sum(answer_key['points'])
    results = []
    failed = 0

    for img_name in os.listdir(args.input_dir):
        if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        try:
            path = os.path.join(args.input_dir, img_name)
            image = cv2.imread(path)

            image = preprocessor.correct_orientation(image)
            image = preprocessor.deskew(image)
            image = preprocessor.enhance_image(image)

            text = ocr.extract_text(image, debug=True, filename=img_name)

            if args.verbose:
                print(f"[DEBUG] OCR Output for {img_name}:\n{text}\n")

            if not text.strip():
                raise ValueError("OCR failed to extract any text.")

            # Extract student ID (optional)
            student_id = os.path.splitext(img_name)[0]
            for line in text.splitlines():
                if 'student' in line.lower() and ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        student_id = parts[1].strip()
                    break

            # Extract answers
            import re

            answers_dict = {}
            for line in text.split('\n'):
                match = re.match(r"^\s*([0-9Oo]+)\s*[:\-]\s*(.+)", line, re.IGNORECASE)
                if match:
                    qid_raw, answer = match.groups()
                    qid = qid_raw.upper().replace('O', '0').zfill(1).lstrip('0')  # Normalize 'O1' → '01' → '1'
                    answers_dict[qid] = answer.strip()

            score, student_answers = grader.grade_student(answers_dict, answer_key)

            results.append({
                "student_id": student_id,
                "image_file": img_name,
                "raw_score": score,
                "total_possible": total_possible,
                "percentage": round((score / total_possible) * 100, 2),
                "answers": student_answers
            })

        except Exception as e:
            failed += 1
            if args.verbose:
                print(f"[ERROR] {img_name}: {str(e)}")

    metadata = {
        "processed_date": datetime.utcnow().isoformat() + "Z",
        "total_images": len(os.listdir(args.input_dir)),
        "successfully_processed": len(results),
        "failed_images": failed,
        "total_questions": len(answer_key)
    }

    report = {
        "metadata": metadata,
        "individual_results": results,
        "class_statistics": utils.compute_statistics(results, total_possible)
    }

    utils.save_json(report, args.output)
    print(f"[INFO] Report saved to {args.output}")

if __name__ == "__main__":
    main()