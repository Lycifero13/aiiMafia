import json
from typing import Dict

from .providers.base import ProviderBase


class ParseError(Exception):
    pass


def _retry_prompt(original_prompt: str, provider: ProviderBase) -> str:
    retry_instruction = "Fix your answer and return ONLY valid JSON."
    combined = f"{original_prompt}\n\n{retry_instruction}"
    return provider.generate(combined)


def parse_json_response(provider: ProviderBase, raw_text: str, expected: str) -> Dict[str, str]:
    """Parse model response expecting JSON. Retry once if parsing fails."""

    def _parse(text: str) -> Dict[str, str]:
        try:
            data = json.loads(text)
            if not isinstance(data, dict):
                raise ParseError("Response is not a JSON object")
            if expected == "day":
                if "speech" not in data or "vote" not in data:
                    raise ParseError("Missing speech or vote keys")
            elif expected == "night":
                if "action" not in data or "target" not in data:
                    raise ParseError("Missing action or target keys")
            return {k: str(v) for k, v in data.items()}
        except json.JSONDecodeError as exc:
            raise ParseError(str(exc))

    try:
        return _parse(raw_text)
    except ParseError:
        retry_text = _retry_prompt(raw_text, provider)
        return _parse(retry_text)
