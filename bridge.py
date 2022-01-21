from Player import *
from Players_VS import *


class bridge:
    @staticmethod
    def player_info(ally):
        player = Player(ally)
        rez = player.write()

        return rez

    @staticmethod
    def players_vs(ally):
        players = []

        for code in ally:
            players.append(Players_VS(code))

        rez = Players_VS.write(players)

        return rez
