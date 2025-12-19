from typing import List

DAY_PROMPT_TEMPLATE = (
    "You are {name}, a player in a Mafia game. Your hidden role is {role}. "
    "Alive players: {alive}. Previous events: {memory}. "
    "Everyone gives exactly one short speech, then votes to eliminate someone. "
    "Reply ONLY with JSON using this schema: {\"speech\": \"short speech\", \"vote\": \"PlayerName\"}. "
    "Pick a vote among the alive players except yourself."
)

NIGHT_PROMPT_TEMPLATE = (
    "You are {name}, a player in a Mafia game. Your hidden role is {role}. "
    "Alive players: {alive}. Previous events: {memory}. "
    "At night you may act based on your role. Allowed actions: kill (Mafia), heal (Doctor), "
    "check (Sheriff), none (Town). Reply ONLY with JSON using this schema: "
    "{\"action\": \"kill|heal|check|none\", \"target\": \"PlayerName\"}. "
    "Choose a valid alive target (can self-heal as Doctor)."
)


def build_day_prompt(name: str, role: str, alive_players: List[str], memory: List[str], speeches: List[str]) -> str:
    memory_text = " | ".join(memory) if memory else "No prior info"
    speech_text = " | ".join(speeches) if speeches else "No speeches yet"
    alive_text = ", ".join(alive_players)
    prompt = DAY_PROMPT_TEMPLATE.format(name=name, role=role, alive=alive_text, memory=f"{memory_text}; Speeches: {speech_text}")
    return prompt


def build_night_prompt(name: str, role: str, alive_players: List[str], memory: List[str]) -> str:
    memory_text = " | ".join(memory) if memory else "No prior info"
    alive_text = ", ".join(alive_players)
    prompt = NIGHT_PROMPT_TEMPLATE.format(name=name, role=role, alive=alive_text, memory=memory_text)
    return prompt
