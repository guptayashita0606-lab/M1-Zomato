from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any


class GroqClientError(RuntimeError):
    """Raised when Groq API call fails."""


class GroqClient:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        timeout_s: float = 30.0,
        temperature: float = 0.2,
        max_tokens: int = 700,
        max_retries: int = 2,
    ) -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.model = model or os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        self.timeout_s = timeout_s
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self._url = "https://api.groq.com/openai/v1/chat/completions"

    def chat_json(self, *, system_instructions: str, user_prompt: str) -> dict[str, Any]:
        if not self.api_key:
            raise GroqClientError("GROQ_API_KEY is not configured.")

        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_prompt},
            ],
        }
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "milestone1-cli/0.1 (+https://local.dev)",
        }

        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            req = urllib.request.Request(self._url, data=body, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                    response_payload = json.loads(resp.read().decode("utf-8"))
                    content = (
                        response_payload.get("choices", [{}])[0]
                        .get("message", {})
                        .get("content", "")
                    )
                    if not content:
                        raise GroqClientError("Groq returned empty completion content.")
                    return json.loads(content)
            except urllib.error.HTTPError as exc:
                error_body = exc.read().decode("utf-8", errors="ignore")
                # Retry only transient provider errors.
                if exc.code in {429, 500, 502, 503, 504} and attempt < self.max_retries:
                    time.sleep(0.6 * (attempt + 1))
                    last_error = exc
                    continue
                raise GroqClientError(
                    f"Groq HTTP error: {exc.code}; body: {error_body[:300]}"
                ) from exc
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                if attempt < self.max_retries:
                    time.sleep(0.6 * (attempt + 1))
                    last_error = exc
                    continue
                raise GroqClientError(f"Groq request failed: {exc}") from exc

        raise GroqClientError(f"Groq request failed after retries: {last_error}")
