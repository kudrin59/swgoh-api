from func import *


class Players_VS:
    def __init__(self, ally):
        player = func.get_info(ally)

        self.name = player['name']
        self.allGM = player['stats'][0]['value']
        self.squadGm = player['stats'][1]['value']
        self.flotGm = player['stats'][2]['value']

    @staticmethod
    def write(player):
        rez = ""
        names = []
        table = [
            ["========= Обзор =========", True],
            ["Мощь\t\t", 0, 0],
            ["Персонажи ГМ", 0, 0],
            ["Флот ГМ\t", 0, 0]
        ]

        for i in range(len(player)):
            names.append(player[i].name)
            row = i + 1
            table[1][row] = player[i].allGM
            table[2][row] = player[i].squadGm
            table[3][row] = player[i].flotGm

        rez += "```{0} vs {1}```".format(names[0], names[1])
        rez += "```"
        for line in table:
            if line[1] == True:
                rez += line[0] + "\n"
            else:
                rez += "{0}\t::\t{1}\tvs\t{2}\n".format(line[0], line[1], line[2])
        rez += "```"

        return rez