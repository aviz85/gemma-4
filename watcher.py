#!/usr/bin/env python3
"""
Watcher: polls ollama list, runs batch_test.py as each gemma4 model becomes available.
"""
import time, subprocess, requests, json
from datetime import datetime

OLLAMA = "/Applications/Ollama.app/Contents/Resources/ollama"
MODELS = ["gemma4:e2b", "gemma4:e4b", "gemma4:26b", "gemma4:31b"]
POLL_SEC = 30
tested = set()


def available_models():
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=5)
        return {m["name"] for m in resp.json().get("models", [])}
    except:
        return set()


def run_test(model):
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🚀 Starting test for {model}")
    subprocess.run(["python3", "/Users/aviz/gemma-4/batch_test.py", model])


print(f"👀 Watching for Gemma 4 models... (polling every {POLL_SEC}s)")
print(f"   Waiting for: {MODELS}\n")

while True:
    avail = available_models()
    for model in MODELS:
        if model in avail and model not in tested:
            tested.add(model)
            run_test(model)

    if tested == set(MODELS):
        print("\n✅ All models tested!")
        break

    remaining = [m for m in MODELS if m not in tested]
    ready_not_tested = [m for m in remaining if m in avail]

    if ready_not_tested:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Ready: {ready_not_tested} | Downloading: {[m for m in remaining if m not in avail]}")
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Still downloading: {remaining}", end="\r")

    time.sleep(POLL_SEC)
