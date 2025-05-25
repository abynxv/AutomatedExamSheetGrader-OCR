# Automated Exam Sheet Grader using OCR

This Python project automates grading of handwritten or printed answer sheets using OCR (Optical Character Recognition). It extracts student answers from scanned images, compares them to an answer key, and generates a detailed report with class statistics.

## Features

- **OCR-based answer extraction** using Tesseract
- **Image preprocessing**: orientation correction, deskewing, enhancement
- **Flexible grading**: supports objective and short-text answers
- **Detailed reports** in JSON format with scores, grades, and analytics

## Installation

### 1. Install Tesseract OCR

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

#### macOS (using Homebrew)
```bash
brew install tesseract
```

#### Windows
1. Download installer from: https://github.com/tesseract-ocr/tesseract/wiki
2. Install and add the install path to your system's PATH
   - Example path: `C:\Program Files\Tesseract-OCR`

**Verify installation:**
```bash
tesseract --version
```

### 2. Python Environment Setup

#### Using venv
```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
pytesseract
opencv-python
numpy
Pillow
scikit-image
```

### 4. Verify Setup

```bash
python main.py --help
tesseract --version
```

## Project Structure

```
project-root/
│
├── main.py
├── requirements.txt
├── README.md
├── sample_data/
│   ├── images/
│   ├── answer_key.csv
│   └── sample_report.json
├── src/
│   ├── preprocessor.py
│   ├── ocr.py
│   ├── grader.py
│   └── utils.py
└── tests/
    └── test_grader.py
```

## Usage

### Basic Command
```bash
python main.py --input_dir sample_data/images --key sample_data/answer_key.csv --output sample_data/report.json
```

### Verbose Debugging
```bash
python main.py --input_dir sample_data/images --key sample_data/answer_key.csv --output sample_data/report.json --verbose
```

## Input Formats

### Answer Key (answer_key.csv)
```csv
question_id,correct_answer,points
1,A,2
2,B,2
3,Photosynthesis,4
4,C,2
5,Mitochondria,2
```

### Answer Sheet Images
- **Supported formats**: `.jpg`, `.png`, `.jpeg`
- **Expected OCR output format**:
  ```
  1: A  
  2: B  
  3: Photosynthesis  
  4: C  
  5: Mitochondria
  ```
## Output Formats

  ![image](https://github.com/user-attachments/assets/f2de450c-a7dd-4001-b295-b33a5a3145a9)
  ![image](https://github.com/user-attachments/assets/dcc7dcce-cb54-4b59-8171-3d427f68f04a)

## Testing

### Running Tests
```bash
python -m unittest discover tests
```

### Test Coverage

The test suite includes:

#### Image Preprocessing
- Orientation correction
- Deskewing
- Image enhancement

#### OCR Extraction
- Extract text accurately from test images

#### Grading Logic
- Handle case-insensitive matching
- Allow partial credit (if applicable)
- Ensure correct score computation

#### Utility Functions
- JSON writing
- Statistics calculation

### Example Test Structure

```python
# tests/test_grader.py
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

```

## Troubleshooting

### OCR Not Extracting Text
- Ensure image quality is sufficient (300 DPI recommended)
- Use grayscale or binarized images
- Test Tesseract manually:
  ```bash
  tesseract path/to/image.png stdout
  ```

### Common Errors

| Error Message | Solution |
|---------------|----------|
| `tesseract is not installed or it's not in PATH` | Install Tesseract and add to system PATH |
| `OCR failed to extract any text` | Check image clarity or preprocessing methods |
| `KeyError during grading` | Ensure answer_key has all question IDs |
| `DeprecationWarning: datetime.utcnow()` | Use `datetime.now(timezone.utc)` instead |

## License

This project is open-source under the MIT License.
