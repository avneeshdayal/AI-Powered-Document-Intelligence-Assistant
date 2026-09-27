"""Starter evaluation script. Add a larger labelled test set before publishing metrics."""
import json
with open("evaluation/questions.json", encoding="utf-8") as f:
    questions = json.load(f)
print(f"Loaded {len(questions)} evaluation questions.")
for i, q in enumerate(questions, 1):
    print(f"{i}. {q['question']} | expected page: {q['expected_page']}")
