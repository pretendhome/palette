from __future__ import annotations


class LocalFallback:
    def handle_blocked(self, reason: str) -> dict:
        return {
            "blocked": True,
            "message": "External research blocked. Using local knowledge only.",
            "reason": reason,
        }

    def handle_rate_limited(self) -> dict:
        return {
            "blocked": True,
            "message": "Perplexity daily limit reached. Using local knowledge only.",
            "reason": "rate_limited",
        }

    def handle_perplexity_error(self, error_message: str) -> dict:
        return {
            "blocked": True,
            "message": "Perplexity is unavailable. Using local knowledge only.",
            "reason": error_message,
        }
