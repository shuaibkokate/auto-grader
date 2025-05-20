import pandas as pd
import textstat

# === Dynamic grading logic based on business rules ===
def dynamic_grade(text):
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

    # Calculate relevance score by matching keywords
    relevance_score = sum(weight for kw, weight in keyword_weights.items() if kw in text_lower)

    # Calculate readability score using Flesch Reading Ease
    try:
        readability = textstat.flesch_reading_ease(text)
        # Normalize readability to a score between 1 and 3 (1 = easy, 3 = hard)
        if readability > 70:
            complexity_score = 1
        elif readability > 50:
            complexity_score = 2
        else:
            complexity_score = 3
    except:
        complexity_score = 2

    # Word count scoring (depth of submission)
    word_count = len(text.split())
    length_score = 1 if word_count > 150 else 0

    # Final score capped at 10
    final_score = min(10, 5 + relevance_score + length_score - complexity_score)

    # Generate feedback
    feedback = (
        f"Content relevance score: {relevance_score}. "
        f"Readability score: {readability:.2f}. Word count: {word_count}."
    )

    return final_score, feedback


def main():
    # Load submissions
    df = pd.read_csv("sample_submissions.csv")

    scores = []
    feedbacks = []

    for submission in df["submission"]:
        score, feedback = dynamic_grade(submission)
        scores.append(score)
        feedbacks.append(feedback)

    df["score"] = scores
    df["feedback"] = feedbacks

    df.to_csv("graded_submissions.csv", index=False)
    print("Grading complete. Results saved to graded_submissions.csv")


if __name__ == "__main__":
    main()
