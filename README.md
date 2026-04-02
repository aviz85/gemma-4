# Gemma 4 Playground

A fast, local web UI for chatting with and comparing [Gemma 4](https://ai.google.dev/gemma) models via [Ollama](https://ollama.com). Everything runs on your machine — no API keys, no cloud, 100% private.

## Features

| | |
|---|---|
| 💬 **Chat** | Streaming responses with Gemma 4's chain-of-thought thinking mode |
| ⚖️ **Compare** | Run the same prompt across all models sequentially, side-by-side results |
| 🗂️ **Conversation history** | Auto-saved to browser IndexedDB — persists across reloads |
| 📊 **Metrics** | Tokens/sec, total tokens, duration per response |
| 🔄 **RTL support** | Per-paragraph auto-detection for Hebrew / Arabic |
| 🌙 **Dark / light mode** | Follows system preference, persisted in localStorage |
| ⚡ **Preset prompts** | One-click benchmarks: math, code, reasoning, creative, multilingual |

## Requirements

- [Node.js](https://nodejs.org) 18+
- [Ollama](https://ollama.com) v0.20.0+ running locally (Gemma 4 requires this version)

## 1 — Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Start the server
ollama serve
```

## 2 — Pull Models

Pull whichever sizes fit your hardware. The app auto-detects all `gemma4*` models.

```bash
ollama pull gemma4:e2b   # 7.2 GB  — edge model, fastest
ollama pull gemma4:e4b   # 9.6 GB  — edge model, default (recommended)
ollama pull gemma4:26b   # 18 GB   — MoE, 4B active params, high quality
ollama pull gemma4:31b   # 20 GB   — dense, best quality
```

> **Apple Silicon:** Metal GPU acceleration is used automatically by Ollama.
> All models support **text + image input** with 128K–256K context window.

## 3 — Run the App

```bash
git clone https://github.com/aviz85/gemma-4.git
cd gemma-4
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

## Usage

### Chat Mode
1. Select a model from the model bar
2. Toggle **Thinking ON/OFF** — enables Gemma 4's extended chain-of-thought reasoning
3. Type a message or pick a preset prompt (Enter to send, Shift+Enter for newline)
4. Click the amber thinking block to expand/collapse the reasoning trace
5. Conversations auto-save — browse history from the **☰ sidebar**

### Compare Mode
1. Click **Compare** in the header (centered tab)
2. Enter a prompt or pick a preset
3. Click **Run All** — models run one at a time to avoid overloading your machine
4. Results appear side-by-side with per-model TPS, token count, and duration
5. Click **Stop** to abort mid-run

### Conversation Sidebar
- Click **☰** (top-left) to open the panel
- Click **New conversation** to start fresh
- Hover any conversation → **🗑** to delete it
- **Clear all** at the bottom (with confirmation)

## Tech Stack

- [Vite](https://vitejs.dev) + [React](https://react.dev) + TypeScript
- [Tailwind CSS v4](https://tailwindcss.com)
- [Ollama Chat API](https://github.com/ollama/ollama/blob/main/docs/api.md) — local streaming
- [Lucide React](https://lucide.dev) icons
- IndexedDB (native browser API) for conversation persistence

## License

MIT
