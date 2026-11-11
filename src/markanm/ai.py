"""
MarkanM AI Integration Layer — Multi-Provider AI for Developer Bots
Supports: OpenAI, Google Gemini, Anthropic Claude, Groq, Sarvam, Mistral,
          Cohere, HuggingFace Inference API, and any Custom HTTP endpoint.
"""
import json
import asyncio
from typing import Optional, List, Dict, Any, Union
from .exceptions import MarkanMError, _mask_sensitive

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False
    import urllib.request
    import urllib.error


# ─────────────────────────────────────────────────────────────────────────────
# Provider Presets
# Each entry: (base_url, chat_endpoint, auth_header, response_parser, request_builder)
# ─────────────────────────────────────────────────────────────────────────────
_PROVIDER_CONFIG = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "endpoint": "/chat/completions",
        "default_model": "gpt-3.5-turbo",
        "format": "openai",
        "auth": "bearer",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "endpoint": "/chat/completions",
        "default_model": "llama3-8b-8192",
        "format": "openai",
        "auth": "bearer",
    },
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "endpoint": "/chat/completions",
        "default_model": "mistral-small-latest",
        "format": "openai",
        "auth": "bearer",
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "endpoint": "/chat/completions",
        "default_model": "deepseek-chat",
        "format": "openai",
        "auth": "bearer",
    },
    "together": {
        "base_url": "https://api.together.xyz/v1",
        "endpoint": "/chat/completions",
        "default_model": "mistralai/Mistral-7B-Instruct-v0.1",
        "format": "openai",
        "auth": "bearer",
    },
    "perplexity": {
        "base_url": "https://api.perplexity.ai",
        "endpoint": "/chat/completions",
        "default_model": "llama-3.1-sonar-small-128k-online",
        "format": "openai",
        "auth": "bearer",
    },
    "sarvam": {
        # Sarvam AI — Indian multilingual models (OpenAI-compatible API)
        # Available models: sarvam-105b, sarvam-105b-conversations
        "base_url": "https://api.sarvam.ai/v1",
        "endpoint": "/chat/completions",
        "default_model": "sarvam-105b",
        "format": "openai",
        "auth": "bearer",
    },
    "anthropic": {
        "base_url": "https://api.anthropic.com/v1",
        "endpoint": "/messages",
        "default_model": "claude-3-haiku-20240307",
        "format": "anthropic",
        "auth": "anthropic",
    },
    "gemini": {
        # Google Gemini REST API
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
        "endpoint": "/models/{model}:generateContent",
        "default_model": "gemini-1.5-flash",
        "format": "gemini",
        "auth": "query_key",
    },
    "cohere": {
        "base_url": "https://api.cohere.ai/v1",
        "endpoint": "/chat",
        "default_model": "command-r",
        "format": "cohere",
        "auth": "bearer",
    },
    "huggingface": {
        "base_url": "https://api-inference.huggingface.co/models",
        "endpoint": "/{model}",
        "default_model": "mistralai/Mistral-7B-Instruct-v0.1",
        "format": "huggingface",
        "auth": "bearer",
    },
    "ollama": {
        # Local Ollama instance
        "base_url": "http://localhost:11434/api",
        "endpoint": "/chat",
        "default_model": "llama3",
        "format": "ollama",
        "auth": "none",
    },
    "openrouter": {
        # OpenRouter — access 100s of models with one API key
        "base_url": "https://openrouter.ai/api/v1",
        "endpoint": "/chat/completions",
        "default_model": "meta-llama/llama-3-8b-instruct:free",
        "format": "openai",
        "auth": "bearer",
    },
}


class AI:
    """
    MarkanM AI Integration Layer — use ANY AI provider in your bot.

    Quick start:
        from markanm.ai import AI
        ai = AI(provider="groq", api_key="gsk_...")
        answer = await ai.generate("What is the capital of India?")

    Supported providers:
        "openai"      — OpenAI GPT (gpt-3.5-turbo, gpt-4o, ...)
        "groq"        — Groq ultra-fast inference (llama3, mixtral, ...)
        "gemini"      — Google Gemini (gemini-1.5-flash, gemini-pro, ...)
        "anthropic"   — Anthropic Claude (claude-3-haiku, claude-3-sonnet, ...)
        "mistral"     — Mistral AI (mistral-small, mistral-large, ...)
        "sarvam"      — Sarvam AI Indian multilingual (sarvam-m, ...)
        "deepseek"    — DeepSeek (deepseek-chat, ...)
        "together"    — Together AI (hundreds of open models)
        "perplexity"  — Perplexity (with live web search)
        "cohere"      — Cohere Command R
        "huggingface" — HuggingFace Inference API
        "ollama"      — Local Ollama (no API key needed)
        "openrouter"  — OpenRouter (access 100s of models, many free)
        "custom"      — Any custom HTTP endpoint (bring your own server)
    """

    def __init__(
        self,
        provider: str = "openai",
        api_key: Union[str, List[str], None] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        system_prompt: str = "You are a helpful assistant.",
        timeout: float = 60.0,
    ):
        self.provider = provider.lower().strip()

        # Handle api_key passed as a list (e.g. api_key=["sk_..."])
        if isinstance(api_key, list):
            self.api_key = api_key[0] if api_key else ""
        else:
            self.api_key = api_key or ""

        self.config = _PROVIDER_CONFIG.get(self.provider)
        self.model = model or (self.config["default_model"] if self.config else "")
        self.base_url = (base_url or (self.config["base_url"] if self.config else "")).rstrip("/")
        self.system_prompt = system_prompt
        self.timeout = timeout

        # Conversation memory: list of {"role": ..., "content": ...}
        self._history: List[Dict[str, str]] = []

    # ─── Public API ──────────────────────────────────────────────────────────

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate a single response (stateless, no history)."""
        if not prompt or not isinstance(prompt, str):
            raise MarkanMError("Prompt must be a non-empty string.")
        sys = system_prompt or self.system_prompt
        return await self._dispatch(prompt, sys, history=[])

    async def chat(self, user_message: str) -> str:
        """
        Multi-turn chat with automatic conversation memory.
        Each call remembers previous messages.

        Usage:
            ai = AI(provider="groq", api_key="...", system_prompt="You are a Python tutor.")
            r1 = await ai.chat("What is a list?")
            r2 = await ai.chat("Give me an example.")  # remembers context!
        """
        self._history.append({"role": "user", "content": user_message})
        response = await self._dispatch(user_message, self.system_prompt, history=self._history[:-1])
        self._history.append({"role": "assistant", "content": response})
        return response

    def reset(self):
        """Clear conversation memory."""
        self._history = []

    # ─── Internal dispatch ────────────────────────────────────────────────────

    async def _dispatch(self, prompt: str, system_prompt: str, history: List[Dict]) -> str:
        if self.provider == "custom":
            return await self._call_custom(prompt, system_prompt, history)

        if not self.config:
            supported = ", ".join(f'"{k}"' for k in _PROVIDER_CONFIG.keys())
            raise MarkanMError(
                f"Unsupported AI provider '{self.provider}'.\n"
                f"Supported providers: {supported}\n"
                f"For any other service, use provider='custom' with base_url='https://...'."
            )

        fmt = self.config["format"]

        if fmt == "openai":
            return await self._call_openai_compat(prompt, system_prompt, history)
        elif fmt == "anthropic":
            return await self._call_anthropic(prompt, system_prompt, history)
        elif fmt == "gemini":
            return await self._call_gemini(prompt, system_prompt, history)
        elif fmt == "cohere":
            return await self._call_cohere(prompt, system_prompt, history)
        elif fmt == "huggingface":
            return await self._call_huggingface(prompt)
        elif fmt == "ollama":
            return await self._call_ollama(prompt, system_prompt, history)
        else:
            raise MarkanMError(f"Unknown provider format: {fmt}")

    # ─── OpenAI-compatible (OpenAI, Groq, Mistral, Sarvam, DeepSeek, Together, Perplexity, OpenRouter) ──

    async def _call_openai_compat(self, prompt: str, system_prompt: str, history: List[Dict]) -> str:
        endpoint = self.base_url + self.config["endpoint"]
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": prompt})

        headers = {"Content-Type": "application/json"}
        if self.config["auth"] == "bearer" and self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {"model": self.model, "messages": messages}
        data = await self._http_post(endpoint, headers, payload)

        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError):
            raise MarkanMError(f"Unexpected response from {self.provider}: {str(data)[:200]}")

    # ─── Anthropic Claude ──────────────────────────────────────────────────────

    async def _call_anthropic(self, prompt: str, system_prompt: str, history: List[Dict]) -> str:
        endpoint = self.base_url + self.config["endpoint"]
        messages = list(history) + [{"role": "user", "content": prompt}]

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
        }
        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "system": system_prompt,
            "messages": messages,
        }
        data = await self._http_post(endpoint, headers, payload)
        try:
            return data["content"][0]["text"].strip()
        except (KeyError, IndexError):
            raise MarkanMError(f"Unexpected Anthropic response: {str(data)[:200]}")

    # ─── Google Gemini ─────────────────────────────────────────────────────────

    async def _call_gemini(self, prompt: str, system_prompt: str, history: List[Dict]) -> str:
        ep_template = self.config["endpoint"].replace("{model}", self.model)
        endpoint = f"{self.base_url}{ep_template}?key={self.api_key}"

        contents = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": contents,
        }
        headers = {"Content-Type": "application/json"}
        data = await self._http_post(endpoint, headers, payload)
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (KeyError, IndexError):
            raise MarkanMError(f"Unexpected Gemini response: {str(data)[:200]}")

    # ─── Cohere ────────────────────────────────────────────────────────────────

    async def _call_cohere(self, prompt: str, system_prompt: str, history: List[Dict]) -> str:
        endpoint = self.base_url + self.config["endpoint"]
        chat_history = []
        for msg in history:
            role = "USER" if msg["role"] == "user" else "CHATBOT"
            chat_history.append({"role": role, "message": msg["content"]})

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        payload = {
            "model": self.model,
            "message": prompt,
            "preamble": system_prompt,
            "chat_history": chat_history,
        }
        data = await self._http_post(endpoint, headers, payload)
        try:
            return data["text"].strip()
        except KeyError:
            raise MarkanMError(f"Unexpected Cohere response: {str(data)[:200]}")

    # ─── HuggingFace Inference API ─────────────────────────────────────────────

    async def _call_huggingface(self, prompt: str) -> str:
        ep_template = self.config["endpoint"].replace("{model}", self.model)
        endpoint = self.base_url + ep_template
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": 512, "return_full_text": False}}
        data = await self._http_post(endpoint, headers, payload)
        try:
            if isinstance(data, list):
                return data[0].get("generated_text", str(data)).strip()
            return str(data).strip()
        except Exception:
            raise MarkanMError(f"Unexpected HuggingFace response: {str(data)[:200]}")

    # ─── Ollama (local) ────────────────────────────────────────────────────────

    async def _call_ollama(self, prompt: str, system_prompt: str, history: List[Dict]) -> str:
        endpoint = self.base_url + self.config["endpoint"]
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": prompt})
        headers = {"Content-Type": "application/json"}
        payload = {"model": self.model, "messages": messages, "stream": False}
        data = await self._http_post(endpoint, headers, payload)
        try:
            return data["message"]["content"].strip()
        except (KeyError, TypeError):
            raise MarkanMError(f"Unexpected Ollama response: {str(data)[:200]}")

    # ─── Custom HTTP endpoint ──────────────────────────────────────────────────

    async def _call_custom(self, prompt: str, system_prompt: str, history: List[Dict]) -> str:
        """
        Call any custom HTTP AI endpoint.
        Sends a POST with JSON body:
          { "prompt": "...", "system": "...", "history": [...], "model": "..." }
        Expects JSON response with "text", "content", "response", or "output" field.
        """
        if not self.base_url:
            raise MarkanMError("For provider='custom', you must provide base_url='https://your-api.com/generate'")
        endpoint = self.base_url
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        payload = {
            "prompt": prompt,
            "system": system_prompt,
            "history": history,
            "model": self.model or "default",
        }
        data = await self._http_post(endpoint, headers, payload)
        for key in ("text", "content", "response", "output", "result", "message", "answer"):
            if key in data and data[key]:
                val = data[key]
                if isinstance(val, dict):
                    return str(val.get("content", val)).strip()
                return str(val).strip()
        raise MarkanMError(f"Could not parse custom endpoint response. Got: {str(data)[:300]}")

    # ─── HTTP helper ───────────────────────────────────────────────────────────

    async def _http_post(self, url: str, headers: Dict, payload: Dict) -> Any:
        if HAS_HTTPX:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                try:
                    res = await client.post(url, json=payload, headers=headers)
                    try:
                        data = res.json()
                    except Exception:
                        data = {}
                    if not res.is_success:
                        err_msg = data.get("error", {})
                        if isinstance(err_msg, dict):
                            err_msg = err_msg.get("message", res.text)
                        raise MarkanMError(f"AI Provider HTTP {res.status_code}: {_mask_sensitive(str(err_msg))}")
                    return data
                except httpx.TimeoutException:
                    raise MarkanMError(f"AI Provider request timed out after {self.timeout}s")
                except httpx.RequestError as exc:
                    raise MarkanMError(f"AI Provider network error: {_mask_sensitive(str(exc))}")
        else:
            def _sync_request():
                body = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(url, data=body, headers=headers, method="POST")
                try:
                    with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                        return json.loads(resp.read().decode("utf-8"))
                except urllib.error.HTTPError as err:
                    try:
                        body_text = err.read().decode("utf-8")
                        err_data = json.loads(body_text)
                        msg = err_data.get("error", {}).get("message", body_text)
                    except Exception:
                        msg = str(err)
                    raise MarkanMError(f"AI Provider HTTP {err.code}: {_mask_sensitive(msg)}")
                except Exception as exc:
                    raise MarkanMError(f"AI Provider error: {_mask_sensitive(str(exc))}")
            return await asyncio.to_thread(_sync_request)
