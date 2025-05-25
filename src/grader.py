import pandas as pd

def load_answer_key(csv_path):
    return pd.read_csv(csv_path)

def grade_student(answers_dict, answer_key_df):
    total = 0
    student_answers = {}
    for _, row in answer_key_df.iterrows():
        qid = str(row['question_id'])
        correct = str(row['correct_answer']).strip().lower()
        points = int(row['points'])
        student_ans = answers_dict.get(qid, "").strip().lower()
        student_answers[qid] = student_ans
        if student_ans == correct:
            total += points
    return total, student_answers