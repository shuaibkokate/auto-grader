# AI Grading System Prototype for 500 Students - Renewable Energy

import pandas as pd
import numpy as np
import random
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Load sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 1. Generate Student Data
def generate_student_data(n=500):
    first_names = ['Ali', 'Sara', 'Omar', 'Lina', 'Zain', 'Noor', 'Hassan', 'Ayesha', 'Khalid', 'Fatima']
    last_names = ['Khan', 'Ahmed', 'Farooq', 'Begum', 'Malik', 'Yousuf', 'Iqbal', 'Rashid', 'Syed', 'Zafar']
    students = []

    mcqs = [
        {"question": "Which of the following is a renewable energy source?", "correct": "Wind"},
        {"question": "What is the main component of solar panels?", "correct": "Silicon"},
        {"question": "Which energy source emits no greenhouse gases?", "correct": "Hydropower"},
    ]

    short_answers = [
        "It helps reduce pollution.",
        "Renewables lower carbon emissions.",
        "Clean energy reduces our carbon footprint.",
        "Helps the environment.",
        "It is sustainable and eco-friendly."
    ]

    essay_templates = [
        "Renewable energy is essential for a sustainable future. It helps reduce greenhouse gases and dependency on fossil fuels. Wind and solar are widely used.",
        "The world needs to move to clean energy. Solar, wind, and hydro are key sources. They are clean, abundant, and better for the planet.",
        "As the world faces climate change, renewable energy is a necessity. It provides clean power and helps reduce global warming.",
        "Fossil fuels are harmful. Renewable energy offers a cleaner alternative. Investing in it can ensure a greener future.",
        "To protect the environment, we must use renewable energy. It is crucial for reducing pollution and saving natural resources."
    ]

    for i in range(n):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        student_id = 1000 + i
        mcq_answers = [random.choice([q["correct"], "Coal", "Oil", "Natural Gas"]) for q in mcqs]
        short = random.choice(short_answers)
        essay = random.choice(essay_templates)

        students.append({
            "student_id": student_id,
            "student_name": name,
            "mcq_1": mcq_answers[0],
            "mcq_2": mcq_answers[1],
            "mcq_3": mcq_answers[2],
            "short_answer": short,
            "essay_answer": essay
        })
    return pd.DataFrame(students)

# 2. Grade MCQs
def grade_mcqs(row):
    score = 0
    if row['mcq_1'] == "Wind": score += 1
    if row['mcq_2'] == "Silicon": score += 1
    if row['mcq_3'] == "Hydropower": score += 1
    return score

# 3. Grade Short Answer (Semantic Similarity)
def grade_short_answer(answer):
    expected = "Renewable energy reduces carbon emissions."
    embeddings = model.encode([answer, expected])
    sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(sim * 10, 2)  # scale to 10 points

# 4. Grade Essay (Basic Rule-Based Scoring)
def grade_essay(answer):
    keywords = ["renewable energy", "sustainable", "solar", "wind", "greenhouse", "climate", "future"]
    score = sum(1 for kw in keywords if kw in answer.lower())
    return min(score * 2, 20)  # out of 20

# Run Grading
if __name__ == '__main__':
    df = generate_student_data(500)
    df['mcq_score'] = df.apply(grade_mcqs, axis=1)
    df['short_score'] = df['short_answer'].apply(grade_short_answer)
    df['essay_score'] = df['essay_answer'].apply(grade_essay)
    df['total_score'] = df['mcq_score'] + df['short_score'] + df['essay_score']

    # Save to CSV
    df.to_csv("graded_student_submissions.csv", index=False)
    print("Grading complete. File saved as 'graded_student_submissions.csv'")
