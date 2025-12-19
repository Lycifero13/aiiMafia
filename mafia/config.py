from __future__ import annotations

import os
import random
from typing import List

from .agents import Agent
from .providers.openai_provider import OpenAIProvider
from .providers.openai_compatible_provider import OpenAICompatibleProvider

ROLES = ["Mafia", "Mafia", "Doctor", "Sheriff", "Town", "Town", "Town", "Town"]
PLAYER_NAMES = [
    "Player1",
    "Player2",
    "Player3",
    "Player4",
    "Player5",
    "Player6",
    "Player7",
    "Player8",
]


def _available_providers():
    providers = []
    if os.environ.get("OPENAI_API_KEY"):
        providers.append(OpenAIProvider())
    if os.environ.get("DEEPSEEK_API_KEY"):
        providers.append(
            OpenAICompatibleProvider(
                base_url="https://api.deepseek.com", api_key_env="DEEPSEEK_API_KEY", model="deepseek-chat"
            )
        )
    if os.environ.get("XAI_API_KEY"):
        providers.append(
            OpenAICompatibleProvider(base_url="https://api.x.ai", api_key_env="XAI_API_KEY", model="grok-beta")
        )
    return providers


def create_players(shuffle: bool = True) -> List[Agent]:
    providers = _available_providers()
    if not providers:
        raise RuntimeError("No providers available. Set at least one API key in environment variables.")

    roles = ROLES.copy()
    if shuffle:
        random.shuffle(roles)

    agents: List[Agent] = []
    for name, role in zip(PLAYER_NAMES, roles):
        provider = random.choice(providers)
        agent = Agent(name=name, role=role, provider=provider)
        agents.append(agent)
    return agents
