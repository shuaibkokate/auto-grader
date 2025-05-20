import pandas as pd
import openai
import os
import random
import textstat

# === CONFIGURATION ===
USE_AI = False  # Set True to use OpenAI, False to use mock grading
CSV_INPUT_PATH = "sample_submissions.csv"
CSV_OUTPUT_PATH = "graded_submissions.csv"

# If using AI, set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-...")  # Replace or set via env variable

# === AI GRADING FUNCTION ===
def ai_grade(text):
    prompt = f"""
    You are an expert grader. Grade this student submission on a scale of 1 to 10 for relevance, clarity, and depth.
    Provide a JSON response like: {{ "score": X, "feedback": "..." }}

    Submission:
    {text}
    """
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=100,
        temperature=0.3
    )
    try:
        result = response.choices[0].text.strip()
        return eval(result)
    except:
        return {"score": 5, "feedback": "Auto-grading failed. Needs manual review."}

# === MORE DYNAMIC MOCK GRADING FUNCTION ===
def mock_grade(text):
    text_lower = text.lower()
    keyword_weights = {
        "industrial": 2,
        "computer": 2,
        "pollution": 1,
        "climate": 2,
        "ai": 2,
        "nutrition": 1,
        "space": 2,
        "mental health": 3,
        "technology": 1,
        "environment": 2
    }

    # Score by keyword match
    keyword_score = sum(weight for keyword, weight in keyword_weights.items() if keyword in text_lower)

    # Readability score using textstat
    try:
        readability_score = textstat.flesch_reading_ease(text)
        complexity_score = 1 if readability_score > 70 else 2 if readability_score > 50 else 3
    except:
        complexity_score = 2

    # Word count evaluation
    word_count = len(text.split())
    length_score = 1 if word_count > 150 else 0

    final_score = min(10, 5 + keyword_score + length_score - complexity_score)

    feedback = f"Submission evaluated based on content relevance and writing ease. Readability score: {readability_score:.2f}, word count: {word_count}."

    return {"score": final_score, "feedback": feedback}

# === MAIN EXECUTION ===
def main():
    df = pd.read_csv(CSV_INPUT_PATH)
    grades = []

    for submission in df["submission"]:
        result = ai_grade(submission) if USE_AI else mock_grade(submission)
        grades.append(result)

    df["score"] = [g["score"] for g in grades]
    df["feedback"] = [g["feedback"] for g in grades]

    df.to_csv(CSV_OUTPUT_PATH, index=False)
    print(f"Graded file saved to {CSV_OUTPUT_PATH}")

if __name__ == "__main__":
    main()
