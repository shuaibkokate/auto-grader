import pandas as pd
import openai
import os

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

# === MOCK GRADING FUNCTION ===
def mock_grade(text):
    if "Industrial Revolution" in text:
        return {"score": 9, "feedback": "Excellent context and clarity about the Industrial Revolution."}
    elif "computers" in text:
        return {"score": 7, "feedback": "Good explanation of computers, could use more depth."}
    elif "Pollution" in text:
        return {"score": 6, "feedback": "Relevant topic with simple language; needs elaboration."}
    else:
        return {"score": 5, "feedback": "Basic response; more detail and structure needed."}

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
