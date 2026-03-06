# Multi-Model MCP for Cursor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Cursor MCP server** that queries OpenAI (GPT-4o), Google (Gemini), and Anthropic (Claude Sonnet) in parallel and returns one answer per provider. Register it in Cursor Agent mode and call a single tool — `query_llm_models` — to get responses from up to three LLMs in one step. Includes a **multi-model-research** skill for a full compare–reconcile–audit workflow.

### Use cases

- Compare GPT, Gemini, and Claude on the same prompt without switching tools
- Run multi-model AI research directly inside Cursor Agent mode
- Get diverse LLM perspectives and reconcile them into one decision-ready output

---

## What this MCP does

- **One tool:** `query_llm_models(prompt, models, system_prompt?)`
- **models:** Any non-empty list of `"openai"`, `"google"`, `"anthropic"` (one, two, or all three).
- **Returns:** A dict mapping each provider name to its reply text.
- **Invocation:** Called as a tool call inside Cursor Agent mode.

All configuration (model names and API keys) comes from a `.env` file. You need your own API keys; this MCP does not provide or store them.

---

## Prerequisites

- **Python 3.10+**
- **Cursor** (with MCP support)
- **API keys** for the providers you use: [OpenAI](https://platform.openai.com/api-keys), [Google AI](https://aistudio.google.com/apikey) (Gemini), [Anthropic](https://console.anthropic.com/). Usage is billed by each provider; this project does not charge anything.

---

## Setup

### 1. Clone and install

```bash
cd cursor_multi_model_mcp
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

- Copy `.env.example` to `.env`.
- In `.env`, set the model names and API keys for the providers you use:
  - OpenAI: `OPENAI_MODEL`, `OPENAI_API_KEY`
  - Google: `GOOGLE_MODEL`, `GOOGLE_API_KEY` (or `GEMINI_API_KEY`)
  - Anthropic: `ANTHROPIC_MODEL`, `ANTHROPIC_API_KEY`
- **Do not commit `.env`.** It is listed in `.gitignore`. Use `.env.example` as a template only.

### 3. Register the MCP in Cursor

Add an entry to `~/.cursor/mcp.json` (create the file if it does not exist). Use the full path to this repo on your machine.

```json
{
  "mcpServers": {
    "multi-model-llm": {
      "command": "/full/path/to/cursor_multi_model_mcp/.venv/bin/python",
      "args": ["/full/path/to/cursor_multi_model_mcp/server.py"]
    }
  }
}
```

Restart Cursor or reload MCP so the new server is picked up.

**Windows:** Use the full path to `.venv\Scripts\python.exe` as `command` and the full path to `server.py` in `args`. In JSON, escape backslashes (`\\`) or use forward slashes. Example (replace `C:/Users/You/cursor_multi_model_mcp` with your repo path):

```json
"multi-model-llm": {
  "command": "C:/Users/You/cursor_multi_model_mcp/.venv/Scripts/python.exe",
  "args": ["C:/Users/You/cursor_multi_model_mcp/server.py"]
}
```

---

## Examples (query_llm_models)

Below, `models` (list) → result (dict: provider name → reply text).

**One model:** `["anthropic"]` → `{"anthropic": "..."}`

**Two models:** `["openai", "google"]` → `{"openai": "...", "google": "..."}`

**All three with system_prompt:** prompt `"Compare REST vs GraphQL for a mobile backend."`, `models: ["openai", "google", "anthropic"]`, `system_prompt: "Keep each answer under 200 words."` → dict with all three keys.

**Deduplication:** `["google", "gemini"]` → one API call; result has a single key `"google"`.

---

## Multi-model-research skill

This repo includes a **skill** that runs a full multi-model research workflow: problem framing, parallel answers from Cursor + 1–3 MCP models, comparison, reconciliation, evidence escalation, and a final audit.

- **Skill file:** `skills/multi-model-research/SKILL.md`
- **How to use:** Copy `skills/multi-model-research` to `~/.cursor/skills/multi-model-research` so Cursor can load it. In **Agent mode**, invoke the skill and say which MCP model(s) you want (openai, google, anthropic — one, two, or all three). The agent will call `query_llm_models` and run the rest of the workflow.

**Example:** "Use the multi-model-research skill. I want to compare OpenAI, Google, and Anthropic. My question: what's the best way to structure a two-week product discovery sprint?"

**Tip:** If Cursor is already using Claude, pick only **openai** and/or **google** from the MCP so you get different vendors.

---

## Run the server manually

For debugging (Cursor normally starts the server via `mcp.json`):

```bash
source .venv/bin/activate
python server.py
```

The server uses stdio; Cursor talks to it via the `command` and `args` in `mcp.json`.

---

## FAQ

**Q: How do I call OpenAI, Gemini, and Claude from Cursor in one step?**  
A: Use the `query_llm_models` tool from this MCP — pass `models: ["openai", "google", "anthropic"]` and get one response per provider.

**Q: Does this work with Cursor Agent mode?**  
A: Yes. Register the MCP in `~/.cursor/mcp.json` and the `query_llm_models` tool is available as a tool call inside any Cursor Agent session.

**Q: Can I use only one or two providers?**  
A: Yes. Pass any non-empty subset: `["openai"]`, `["google", "anthropic"]`, or all three. Only the providers you include are called.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file.
