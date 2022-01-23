from swgoh.Player import *


class bridge:
    @staticmethod
    def player_info(ally):
        player = Player(ally)
        rez = player.write()

        return rez

    @staticmethod
    def players_compare(ally):
        players = []

        for code in ally:
            players.append(Player(code))

        rez = Player.compare(players)

        return rez
