"""
Multi-model MCP server for the multi-model research workflow.
Single tool: query_llm_models(prompt, models, system_prompt?) for openai, google, and/or anthropic.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import FastMCP

_env_dir = Path(__file__).resolve().parent
load_dotenv(_env_dir / ".env")

mcp = FastMCP(name="multi-model-llm")


def _require_env(name: str) -> str:
    val = os.environ.get(name)
    if not val:
        raise ValueError(f"{name} is not set. Define it in .env (e.g. {_env_dir / '.env'}) or in ~/.cursor/mcp.json env block.")
    return val


def _openai_completion(prompt: str, system_prompt: str | None) -> str:
    from openai import BadRequestError, OpenAI

    client = OpenAI(api_key=_require_env("OPENAI_API_KEY"))
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    kwargs: dict = {
        "model": _require_env("OPENAI_MODEL"),
        "messages": messages,
    }
    # Use temperature/reasoning_effort when supported; some models (e.g. o1) only allow defaults
    try:
        resp = client.chat.completions.create(
            **kwargs,
            temperature=0.3,
            reasoning_effort="high",
        )
    except BadRequestError:
        resp = client.chat.completions.create(**kwargs)
    if not resp.choices:
        return ""
    return (resp.choices[0].message.content or "").strip()


def _google_completion(prompt: str, system_prompt: str | None) -> str:
    from google import genai
    from google.genai import types

    key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY is not set. Define in .env or ~/.cursor/mcp.json env block.")
    client = genai.Client(api_key=key)
    config = types.GenerateContentConfig(temperature=0.3, system_instruction=system_prompt) if system_prompt else types.GenerateContentConfig(temperature=0.3)
    resp = client.models.generate_content(
        model=_require_env("GOOGLE_MODEL"),
        contents=prompt,
        config=config,
    )
    if not resp.candidates:
        return ""
    c0 = resp.candidates[0]
    if not c0.content or not c0.content.parts:
        return ""
    return (c0.content.parts[0].text or "").strip()


def _anthropic_completion(prompt: str, system_prompt: str | None) -> str:
    import anthropic

    client = anthropic.Anthropic(api_key=_require_env("ANTHROPIC_API_KEY"))
    kwargs = {
        "model": _require_env("ANTHROPIC_MODEL"),
        "max_tokens": 8192,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system_prompt:
        kwargs["system"] = system_prompt
    resp = client.messages.create(**kwargs)
    if not resp.content:
        return ""
    first = resp.content[0]
    return (getattr(first, "text", None) or "").strip()


def _normalize_model(m: str) -> str:
    m = m.strip().lower()
    if m == "openai":
        return "openai"
    if m in ("google", "gemini"):
        return "google"
    if m == "anthropic" or m.startswith("claude"):
        return "anthropic"
    raise ValueError(f"Unsupported model: {m}. Use 'openai', 'google', or 'anthropic'.")


def _query_one(prompt: str, model: str, system_prompt: str | None) -> str:
    key = _normalize_model(model)
    if key == "openai":
        return _openai_completion(prompt, system_prompt)
    if key == "google":
        return _google_completion(prompt, system_prompt)
    return _anthropic_completion(prompt, system_prompt)


@mcp.tool(
    description="Call one or more of OpenAI (GPT), Google (Gemini), and Anthropic (Claude) with the same prompt. models: any non-empty list of \"openai\", \"google\", \"anthropic\" (e.g. [\"anthropic\"], [\"openai\", \"google\"], or all three). Returns dict of model name to reply text.",
)
def query_llm_models(
    prompt: str,
    models: list[str],
    system_prompt: str | None = None,
) -> dict[str, str]:
    if not models:
        raise ValueError(
            "models must be a non-empty list of 'openai', 'google', 'anthropic' "
            "(e.g. [\"openai\"], [\"google\", \"anthropic\"], or [\"openai\", \"google\", \"anthropic\"])."
        )
    result: dict[str, str] = {}
    for m in models:
        key = _normalize_model(m)
        if key in result:
            continue
        result[key] = _query_one(prompt, m, system_prompt)
    return result


if __name__ == "__main__":
    mcp.run()
