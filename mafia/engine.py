from __future__ import annotations

import random
from typing import Dict, List, Optional

from .agents import Agent

MAFIA_ROLE = "Mafia"
DOCTOR_ROLE = "Doctor"
SHERIFF_ROLE = "Sheriff"


class MafiaGame:
    def __init__(self, players: List[Agent]):
        self.players = players
        self.alive = set(agent.name for agent in players)
        self.day_count = 1

    def _get_agent(self, name: str) -> Optional[Agent]:
        for agent in self.players:
            if agent.name == name:
                return agent
        return None

    def _alive_agents(self) -> List[Agent]:
        return [p for p in self.players if p.name in self.alive]

    def _log(self, message: str) -> None:
        print(message)

    def _apply_vote(self, votes: Dict[str, str]) -> Optional[str]:
        tally: Dict[str, int] = {}
        for voter, target in votes.items():
            if target not in self.alive or target == voter:
                continue
            tally[target] = tally.get(target, 0) + 1
        if not tally:
            return None
        max_votes = max(tally.values())
        candidates = [name for name, count in tally.items() if count == max_votes]
        candidates.sort()
        return random.choice(candidates)

    def _mafia_target(self, night_actions: Dict[str, Dict[str, str]]) -> Optional[str]:
        mafia_votes: Dict[str, int] = {}
        for name, action in night_actions.items():
            if action.get("action") == "kill":
                target = action.get("target")
                if target in self.alive:
                    mafia_votes[target] = mafia_votes.get(target, 0) + 1
        if not mafia_votes:
            return None
        max_votes = max(mafia_votes.values())
        candidates = [t for t, count in mafia_votes.items() if count == max_votes]
        candidates.sort()
        return random.choice(candidates)

    def _doctor_target(self, night_actions: Dict[str, Dict[str, str]]) -> Optional[str]:
        for _, action in night_actions.items():
            if action.get("action") == "heal":
                return action.get("target")
        return None

    def _sheriff_target(self, night_actions: Dict[str, Dict[str, str]]) -> Optional[str]:
        for _, action in night_actions.items():
            if action.get("action") == "check":
                return action.get("target")
        return None

    def _check_victory(self) -> Optional[str]:
        alive_agents = self._alive_agents()
        mafia_alive = [p for p in alive_agents if p.role == MAFIA_ROLE]
        town_alive = [p for p in alive_agents if p.role != MAFIA_ROLE]
        if not mafia_alive:
            return "Town"
        if len(mafia_alive) >= len(town_alive):
            return "Mafia"
        return None

    def night_phase(self) -> None:
        self._log(f"--- Night {self.day_count} ---")
        actions: Dict[str, Dict[str, str]] = {}
        alive_names = list(self.alive)
        for agent in self._alive_agents():
            if agent.role == "Town":
                continue
            result = agent.observe_night(alive_names)
            actions[agent.name] = result

        mafia_target = self._mafia_target(actions)
        doctor_target = self._doctor_target(actions)
        sheriff_target = self._sheriff_target(actions)

        death = None
        if mafia_target and mafia_target != doctor_target:
            death = mafia_target
            self.alive.discard(death)
        sheriff_result = None
        if sheriff_target and sheriff_target in self.alive:
            sheriff_agent = self._get_agent(sheriff_target)
            if sheriff_agent:
                sheriff_result = f"{sheriff_target} is {'Mafia' if sheriff_agent.role == MAFIA_ROLE else 'Not Mafia'}"

        self._log(f"Mafia targeted: {mafia_target or 'no one'}")
        self._log(f"Doctor healed: {doctor_target or 'no one'}")
        if sheriff_result:
            self._log(f"Sheriff investigated: {sheriff_result}")
        if death:
            self._log(f"{death} was eliminated during the night.")
        else:
            self._log("No one died tonight.")

        for agent in self._alive_agents():
            if mafia_target:
                agent.adjust_suspicion(mafia_target, 0.1)
            if sheriff_result:
                agent.record_memory(f"Sheriff info: {sheriff_result}")

    def day_phase(self) -> None:
        self._log(f"--- Day {self.day_count} ---")
        speeches: List[str] = []
        votes: Dict[str, str] = {}
        alive_names = list(self.alive)

        for agent in self._alive_agents():
            observation = agent.observe_day(alive_names, speeches)
            speech = observation.get("speech", "")
            vote = observation.get("vote", "")
            speeches.append(f"{agent.name}: {speech}")
            votes[agent.name] = vote
            agent.record_memory(f"Spoke: {speech}")
            self._log(f"{agent.name} says: {speech}")

        elimination = self._apply_vote(votes)
        if elimination:
            self.alive.discard(elimination)
            self._log(f"{elimination} was voted out by the town.")
        else:
            self._log("No one was eliminated today.")

        for agent in self._alive_agents():
            if elimination:
                agent.adjust_suspicion(elimination, 0.2)

    def reveal_roles(self) -> None:
        self._log("--- Final Roles ---")
        for agent in self.players:
            status = "alive" if agent.name in self.alive else "eliminated"
            self._log(f"{agent.name}: {agent.role} ({status})")

    def play(self) -> None:
        self._log("Starting AI Mafia!")
        winner = None
        while not winner:
            self.night_phase()
            winner = self._check_victory()
            if winner:
                break
            self.day_phase()
            winner = self._check_victory()
            self.day_count += 1
        self._log(f"Winner: {winner}")
        self.reveal_roles()
