from Player import *
from Players_VS import *


class bridge:
    @staticmethod
    def player_info(ally):
        ally = [874672511]

        player = Player(ally)
        player.write()

    @staticmethod
    def players_vs(ally):
        ally = [874672511, 484137946]

        players = []

        for code in ally:
            players.append(Players_VS(code))

        Players_VS.write(players)
