from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .providers.base import ProviderBase
from .prompts import build_day_prompt, build_night_prompt
from .parsing import parse_json_response


@dataclass
class Agent:
    name: str
    role: str
    provider: ProviderBase
    memory: List[str] = field(default_factory=list)
    suspicion: Dict[str, float] = field(default_factory=dict)

    def record_memory(self, entry: str) -> None:
        self.memory.append(entry)

    def adjust_suspicion(self, target: str, delta: float) -> None:
        self.suspicion[target] = self.suspicion.get(target, 0.0) + delta

    def observe_day(self, alive_players: List[str], speeches: List[str]) -> Dict[str, str]:
        prompt = build_day_prompt(self.name, self.role, alive_players, self.memory, speeches)
        response = self.provider.generate(prompt)
        return parse_json_response(self.provider, response, expected="day")

    def observe_night(self, alive_players: List[str]) -> Dict[str, str]:
        prompt = build_night_prompt(self.name, self.role, alive_players, self.memory)
        response = self.provider.generate(prompt)
        return parse_json_response(self.provider, response, expected="night")
