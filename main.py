import random
from dotenv import load_dotenv

from mafia.config import create_players
from mafia.engine import MafiaGame


def main():
    load_dotenv()
    random.seed()
    players = create_players()
    game = MafiaGame(players)
    game.play()


if __name__ == "__main__":
    main()
