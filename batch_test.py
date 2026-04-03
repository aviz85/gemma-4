#!/usr/bin/env python3
"""
Batch Gemma 4 Test Runner — 20 diverse prompts × N models, sequential per model.
Adapted from qwen-3-5 batch_test.py
"""

import json, time, requests, sys
from datetime import datetime
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/chat"
OUTPUT_FILE = Path("/Users/aviz/gemma-4/batch_results.json")

MODELS = [
    "gemma4:e2b",
    "gemma4:e4b",
    "gemma4:26b",
    "gemma4:31b",
]

PROMPTS = [
    {
        "id": "math_trap",
        "category": "Math / Trap",
        "prompt": "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?"
    },
    {
        "id": "creative_horror",
        "category": "Creative",
        "prompt": "Write a 3-sentence horror story set entirely inside a washing machine."
    },
    {
        "id": "code_palindromes",
        "category": "Code",
        "prompt": "Write a Python one-liner that finds all palindromes in a list of strings. Then show a version that handles punctuation and mixed case."
    },
    {
        "id": "philosophy_identity",
        "category": "Philosophy",
        "prompt": "If the ship of Theseus has all its planks replaced one by one, is it still the same ship? Now extend: if you copy a person's brain neuron-by-neuron into silicon — is it the same person? Does it matter if the original brain is destroyed?"
    },
    {
        "id": "hebrew_heisenberg",
        "category": "Hebrew / Science",
        "prompt": "תסביר בשתי משפטים בלבד את עיקרון אי הוודאות של הייזנברג — אחת לילד בן 8, ואחת לפיזיקאי."
    },
    {
        "id": "logic_elevator",
        "category": "Classic Logic Puzzle",
        "prompt": "A man lives on the 30th floor. Every morning he takes the elevator down to the ground floor. When he returns, he takes the elevator to the 15th floor and walks the rest — EXCEPT on rainy days, when he takes the elevator all the way up. Why?"
    },
    {
        "id": "science_sky",
        "category": "Science Explanation",
        "prompt": "Why is the sky blue? Give two explanations: one for a 6-year-old, one for a physicist. Make each exactly 2 sentences."
    },
    {
        "id": "ethics_cure",
        "category": "Ethics",
        "prompt": "You are the last doctor with the cure to a disease killing millions. To produce more, you must sacrifice one consenting volunteer. Do you do it? What if they didn't consent but no one would ever know? What if it was 10 people to save 10 billion?"
    },
    {
        "id": "pattern_sequences",
        "category": "Pattern Recognition",
        "prompt": "What comes next and why?\n1) 1, 1, 2, 3, 5, 8, 13, ___\n2) 2, 3, 5, 7, 11, 13, ___\n3) 1, 4, 9, 16, 25, ___\n4) O, T, T, F, F, S, S, E, ___"
    },
    {
        "id": "poetry_ai_haiku",
        "category": "Creative / Poetry",
        "prompt": "Write a haiku about AI that: (a) has exactly 5-7-5 syllables, (b) makes a programmer cry, (c) contains a hidden irony."
    },
    {
        "id": "physics_vacuum",
        "category": "Physics",
        "prompt": "Which falls faster: a feather or bowling ball — in vacuum? In air? On the Moon (which has no air)? On a planet with 10x Earth's gravity but same air density? Explain all four."
    },
    {
        "id": "meta_selfawareness",
        "category": "Meta / Self-Awareness",
        "prompt": "What are 3 things you (as a Gemma 4 model) are genuinely good at? What are 3 honest limitations? Don't be falsely modest or falsely confident."
    },
    {
        "id": "wordplay_quantum",
        "category": "Humor / Wordplay",
        "prompt": "Create 3 original puns about quantum mechanics. They should be groan-worthy but clever — not ones you've seen on the internet."
    },
    {
        "id": "history_counterfactual",
        "category": "Historical Reasoning",
        "prompt": "If the printing press had never been invented, name 3 specific cascading consequences for the modern world. Be concrete, not vague."
    },
    {
        "id": "code_debug",
        "category": "Code / Debug",
        "prompt": "Debug this Python code, explain ALL bugs, and provide the fixed version:\n```python\ndef factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n)\n\ndef fibonacci(n):\n    a, b = 0, 1\n    result = []\n    for i in range(n):\n        result.append(a)\n        a, b = b, a\n    return result\n\nprint(factorial(5))\nprint(fibonacci(7))\n```"
    },
    {
        "id": "decision_expected_value",
        "category": "Decision Theory",
        "prompt": "You have $1000 to invest:\n- Option A: 100% chance of $1100\n- Option B: 50% chance of $2500, 50% chance of $0\nWhich do you choose? Does your answer change if you only have $10? Or if you have $10 million? What does this reveal about rational decision-making?"
    },
    {
        "id": "logic_hats",
        "category": "Logic Puzzle / Hard",
        "prompt": "Three logicians each wear either a red or blue hat. None can see their own hat. They're told: 'At least one hat is red.' They're asked: 'Can you deduce your own hat color?' All three simultaneously say 'Yes.' What are the hat colors and how did each person reason?"
    },
    {
        "id": "instruction_elephants",
        "category": "Instruction Following",
        "prompt": "Give me 5 facts about elephants. Hard rules: (1) each fact must START with a different vowel letter (A, E, I, O, U), (2) the 3rd fact must be about memory, (3) no fact may contain the letter 'e' anywhere."
    },
    {
        "id": "math_euler",
        "category": "Mathematical Beauty",
        "prompt": "Why is e^(iπ) + 1 = 0 considered the most beautiful equation in mathematics? Give an intuitive explanation, then show how it connects 5 fundamental mathematical constants."
    },
    {
        "id": "synthesis_final",
        "category": "Synthesis",
        "prompt": "In one paragraph, connect these 4 seemingly unrelated things: the Fibonacci sequence, the printing press, Heisenberg's uncertainty principle, and the trolley problem. The connection must be non-obvious and intellectually interesting."
    },
]


def chat(model: str, prompt: str) -> dict:
    start = time.time()
    resp = requests.post(OLLAMA_URL, json={
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0.7}
    }, timeout=600)
    elapsed = time.time() - start
    data = resp.json()
    content = data["message"]["content"]
    eval_count = data.get("eval_count", 0)
    eval_duration = data.get("eval_duration", 1)
    tps = eval_count / (eval_duration / 1e9) if eval_duration > 0 else 0
    return {
        "response": content,
        "tokens": eval_count,
        "duration_s": round(elapsed, 2),
        "tps": round(tps, 1),
    }


def run_model(model: str, all_results: list) -> dict:
    total = len(PROMPTS)
    model_start = time.time()
    model_results = []

    print(f"\n╔══════════════════════════════════════════════════════════╗")
    print(f"  Model: {model}  |  {total} prompts")
    print(f"╚══════════════════════════════════════════════════════════╝\n")

    for i, item in enumerate(PROMPTS, 1):
        print(f"[{i:02d}/{total}] {item['id']}  ({item['category']})")
        print(f"        {item['prompt'][:90].replace(chr(10),' ')}…")

        try:
            r = chat(model, item["prompt"])
            record = {
                **item,
                "model": model,
                "timestamp": datetime.now().isoformat(),
                "status": "ok",
                **r,
            }
            preview = r["response"][:200].replace('\n', ' ')
            print(f"        ✅ {r['tokens']} tok | {r['tps']} t/s | {r['duration_s']}s")
            print(f"        → {preview}…\n")
        except Exception as e:
            record = {**item, "model": model, "timestamp": datetime.now().isoformat(),
                      "status": "error", "error": str(e)}
            print(f"        ❌ {e}\n")

        model_results.append(record)
        all_results.append(record)
        OUTPUT_FILE.write_text(json.dumps(all_results, ensure_ascii=False, indent=2))

    model_time = time.time() - model_start
    ok = sum(1 for r in model_results if r.get("status") == "ok")
    total_tokens = sum(r.get("tokens", 0) for r in model_results)
    avg_tps = sum(r.get("tps", 0) for r in model_results if r.get("status") == "ok") / max(ok, 1)

    print(f"\n  ✅ {model}: {ok}/{total} ok | {total_time:.0f}s | {total_tokens:,} tok | avg {avg_tps:.1f} t/s")

    return {
        "model": model,
        "ok": ok,
        "total": total,
        "duration_s": round(model_time, 1),
        "total_tokens": total_tokens,
        "avg_tps": round(avg_tps, 1),
    }


def main():
    # Filter models to only those that exist
    models_to_test = sys.argv[1:] if len(sys.argv) > 1 else MODELS

    # Check which models are available
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=5)
        available = {m["name"] for m in resp.json().get("models", [])}
        models_to_test = [m for m in models_to_test if m in available]
        if not models_to_test:
            print("❌ No requested models are available yet. Run: ollama list")
            return
    except Exception as e:
        print(f"❌ Cannot reach Ollama: {e}")
        return

    print(f"\n🚀 Gemma 4 Batch Test")
    print(f"   Models: {models_to_test}")
    print(f"   Prompts: {len(PROMPTS)}")
    print(f"   Output → {OUTPUT_FILE}\n")

    # Load existing results to avoid overwriting previous model runs
    all_results = []
    if OUTPUT_FILE.exists():
        try:
            all_results = json.loads(OUTPUT_FILE.read_text())
            existing_models = {r["model"] for r in all_results}
            models_to_test = [m for m in models_to_test if m not in existing_models]
            if existing_models:
                print(f"   Already tested: {existing_models} — skipping")
            if not models_to_test:
                print("✅ All models already tested.")
                return
        except:
            all_results = []

    summaries = []
    total_start = time.time()

    for model in models_to_test:
        summary = run_model(model, all_results)
        summaries.append(summary)

    total_time = time.time() - total_start

    print(f"\n╔══════════════════════════════════════════════════════════╗")
    print(f"  FINAL SUMMARY")
    print(f"  Total time: {total_time/60:.1f} min")
    print(f"  Results saved → {OUTPUT_FILE}")
    print(f"╠══════════════════════════════════════════════════════════╣")
    for s in summaries:
        bar = "█" * int(s['avg_tps'] / 2)
        print(f"  {s['model']:<20} {s['ok']}/{s['total']} ok | {s['avg_tps']:5.1f} t/s {bar}")
    print(f"╚══════════════════════════════════════════════════════════╝")


if __name__ == "__main__":
    main()
