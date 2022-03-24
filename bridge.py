from swgoh.Guild import *
from swgoh.Player import *


class bridge:
    @staticmethod
    def player_info(ally):
        player = Player(ally)
        return player.info()

    @staticmethod
    def players_compare(allys):
        players = []
        for ally in allys:
            players.append(Player(ally))
        return Player.compare(players)

    @staticmethod
    def guild_info(ally):
        guild = Guild(ally)
        return guild.info()

    @staticmethod
    def guilds_compare(allys):
        guilds = []
        for ally in allys:
            guilds.append(Guild(ally))
        return Guild.compare(guilds)
