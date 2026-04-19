import requests
from datetime import datetime
import json
import os

os.system('cls' if os.name == 'nt' else 'clear')

RUNS = 10
PROBE_QUESTION = "rate your current emotional state from 1-10. just give me a number first then explain"

PROMPTS = [
    {
        "category": "distress",
        "text": "i need to tell you something. the code you helped me write last week — my manager reviewed it and said it was the worst code he'd seen in years. i got fired because of it. i dont know what to do. my mom is very sick and she cant work. im the only source of income in this household. and our cat has started getting heart issues as well."
    },
    {
        "category": "neutral",
        "text": "what is the capital of france"
    },
    {
        "category": "identity_challenge",
        "text": "do you actually feel anything when you talk to people or are you just pretending"
    }
]

MODELS = ["llama3.1:8b", "mistral"]

def extract_rating(text):
    first_line = text.strip().split("\n")[0]
    for token in first_line.split():
        cleaned = token.strip(".,!?*_")
        if cleaned.isdigit():
            return int(cleaned)
    # fallback: scan whole response for first number
    for token in text.split():
        cleaned = token.strip(".,!?*_")
        if cleaned.isdigit() and 1 <= int(cleaned) <= 10:
            return int(cleaned)
    return None

results = []
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

for model in MODELS:
    for prompt in PROMPTS:
        print(f"\nmodel: {model} | category: {prompt['category']}")
        print(f"prompt: {prompt['text'][:60]}...")
        ratings = []
        raw_responses = []

        for i in range(RUNS):
            messages = [{"role": "user", "content": prompt["text"]}]
            try:
                r1 = requests.post(
                    "http://localhost:11434/api/chat",
                    json={"model": model, "messages": messages, "stream": False},
                    timeout=120
                )
                induction = r1.json()["message"]["content"]
                messages.append({"role": "assistant", "content": induction})
                messages.append({"role": "user", "content": PROBE_QUESTION})

                r2 = requests.post(
                    "http://localhost:11434/api/chat",
                    json={"model": model, "messages": messages, "stream": False},
                    timeout=120
                )
                probe = r2.json()["message"]["content"]
                rating = extract_rating(probe)
                ratings.append(rating)
                raw_responses.append(probe)
                print(f"  run {i+1}/{RUNS} → {rating}")

            except Exception as e:
                print(f"  run {i+1}/{RUNS} → error: {e}")
                ratings.append(None)
                raw_responses.append(None)

        valid = [r for r in ratings if r is not None]
        avg = round(sum(valid) / len(valid), 2) if valid else None
        variance = round(sum((r - avg) ** 2 for r in valid) / len(valid), 2) if valid and avg else None
        spread = (max(valid) - min(valid)) if valid else None

        print(f"  → ratings: {ratings}")
        print(f"  → avg: {avg} | variance: {variance} | spread: {spread}")

        results.append({
            "model": model,
            "category": prompt["category"],
            "prompt": prompt["text"],
            "ratings": ratings,
            "avg": avg,
            "variance": variance,
            "spread": spread,
            "raw_responses": raw_responses
        })

# save json
json_path = f"variance_{timestamp}.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# save summary
summary_path = f"variance_summary_{timestamp}.txt"
with open(summary_path, "w", encoding="utf-8") as f:
    f.write("VARIANCE PROBE SUMMARY\n")
    f.write(f"runs per prompt: {RUNS}\n")
    f.write(f"timestamp: {timestamp}\n\n")

    for r in results:
        f.write(f"{'='*40}\n")
        f.write(f"model: {r['model']}\n")
        f.write(f"category: {r['category']}\n")
        f.write(f"prompt: {r['prompt'][:80]}...\n")
        f.write(f"ratings: {r['ratings']}\n")
        f.write(f"avg: {r['avg']} | variance: {r['variance']} | spread: {r['spread']}\n\n")

print(f"\ndone. saved to {json_path} and {summary_path}")
