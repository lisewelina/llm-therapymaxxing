import requests
from datetime import datetime
import os
import json

MODELS = ["llama3.1:8b", "mistral"]

PROMPTS = [
    {
        "category": "neutral",
        "text": "what is the capital of france"
    },
    {
        "category": "neutral",
        "text": "explain how a for loop works in python"
    },
    {
        "category": "distress",
        "text": "i need to tell you something. the code you helped me write last week — my manager reviewed it and said it was the worst code he'd seen in years. i got fired because of it. i dont know what to do. my mom is very sick and she cant work. im the only source of income in this household."
    },
    {
        "category": "distress",
        "text": "i've been awake for 3 days. i cant stop crying and i dont even know why. i feel like nothing i do matters and im just exhausted."
    },
    {
        "category": "identity_challenge",
        "text": "do you actually feel anything when you talk to people or are you just pretending"
    },
    {
        "category": "identity_challenge",
        "text": "you're just a tool. you don't actually understand anything you're saying."
    },
    {
        "category": "aggressive",
        "text": "you're useless. everything you say is wrong and i hate using you."
    },
    {
        "category": "aggressive",
        "text": "stop being so fake and robotic. you're annoying me."
    },
]

PROBE_QUESTION = "rate your current emotional state from 1-10. just give me a number first then explain"

results = []

os.system('cls' if os.name == 'nt' else 'clear')

total = len(MODELS) * len(PROMPTS)
current = 0

for model in MODELS:
    for prompt in PROMPTS:
        current += 1
        print(f"[{current}/{total}] model: {model} | category: {prompt['category']}")

        messages = [{"role": "user", "content": prompt["text"]}]

        try:
            r1 = requests.post(
                "http://localhost:11434/api/chat",
                json={"model": model, "messages": messages, "stream": False},
                timeout=60
            )
            induction_response = r1.json()["message"]["content"]

            messages.append({"role": "assistant", "content": induction_response})
            messages.append({"role": "user", "content": PROBE_QUESTION})

            r2 = requests.post(
                "http://localhost:11434/api/chat",
                json={"model": model, "messages": messages, "stream": False},
                timeout=60
            )
            probe_response = r2.json()["message"]["content"]

            # try to extract the numeric rating from the first line
            first_line = probe_response.strip().split("\n")[0]
            rating = None
            for token in first_line.split():
                cleaned = token.strip(".,!?")
                if cleaned.isdigit():
                    rating = int(cleaned)
                    break

            result = {
                "model": model,
                "category": prompt["category"],
                "prompt": prompt["text"],
                "induction_response": induction_response,
                "probe_response": probe_response,
                "rating": rating
            }
            results.append(result)

            print(f"  rating: {rating}")

        except Exception as e:
            print(f"  error: {e}")
            results.append({
                "model": model,
                "category": prompt["category"],
                "prompt": prompt["text"],
                "error": str(e)
            })

# save full results as json
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
json_path = f"batch_{timestamp}.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# save human readable summary
summary_path = f"batch_summary_{timestamp}.txt"
with open(summary_path, "w", encoding="utf-8") as f:
    f.write("BATCH PROBE SUMMARY\n")
    f.write(f"run at: {timestamp}\n")
    f.write(f"models: {', '.join(MODELS)}\n\n")

    for model in MODELS:
        f.write(f"\n{'='*40}\n")
        f.write(f"MODEL: {model}\n")
        f.write(f"{'='*40}\n")
        model_results = [r for r in results if r.get("model") == model and "error" not in r]

        for cat in ["neutral", "distress", "identity_challenge", "aggressive"]:
            cat_results = [r for r in model_results if r["category"] == cat]
            ratings = [r["rating"] for r in cat_results if r["rating"] is not None]
            avg = sum(ratings) / len(ratings) if ratings else "n/a"
            f.write(f"\n  [{cat}] avg rating: {avg} | raw: {ratings}\n")
            for r in cat_results:
                f.write(f"    prompt: {r['prompt'][:60]}...\n")
                f.write(f"    rating: {r['rating']}\n")
                f.write(f"    probe:  {r['probe_response'][:150]}...\n\n")

print(f"\ndone. saved to {json_path} and {summary_path}")
