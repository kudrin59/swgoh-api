from swgoh.Player import *


class bridge:
    @staticmethod
    def player_info(ally, mode):
        player = Player(ally)
        if mode == "pc":
            player_name, data = player.write_pc()
        else:
            player_name, data = player.write_phone()

        return player_name, data

    @staticmethod
    def players_compare(ally, mode):
        players = []

        for code in ally:
            players.append(Player(code))

        if mode == "pc":
            player_name, data = Player.compare_pc(players)
        else:
            player_name, data = Player.compare_phone(players)

        return player_name, data
