from swgoh.func import *


class Player:
    def __init__(self, ally):
        player = func.get_player(ally)

        self.name = player['name']
        self.guildName = player['guildName']
        self.allGM = player['stats'][0]['value']

        self.top80gm = func.get_top80(player['roster'])

        self.squadGm = player['stats'][1]['value']
        self.flotGm = player['stats'][2]['value']
        self.zetas, self.omicrons, self.omicron_units = func.get_zeta_omicron(player['roster'])

        self.ga_lyga = func.get_ga(player['grandArena'])

        self.squadRank = player['arena']['char']['rank']
        self.teamSquad = func.get_arena_squad(player)

        self.flotRank = player['arena']['ship']['rank']
        self.flotCapital, self.flotStart, self.flotReinforcement = func.get_arena_ship(player)

        self.capitals = func.get_capitals(player['roster'])

        self.toons = func.get_toons_compare(player['roster'])

        self.toons1, self.toons2, self.toons3, self.toons4 = func.get_toons(player['roster'])

        self.gears = func.get_gears(player['roster'])

        self.mods = func.get_mods(player['roster'])

    def write(self):
        rez = ""
        rez += "```==== Обзор ====\n"
        rez += "Ник (Гильдия)\t::\t{} ({})\n".format(self.name, self.guildName)
        rez += "Мощь \t\t\t::\t{}\n".format(self.allGM)
        rez += "Персонажи ГМ \t::\t{}\n".format(self.squadGm)
        rez += "Флот ГМ  \t\t::\t{}\n".format(self.flotGm)
        rez += "Дзет \t\t\t::\t{}\n".format(self.zetas)
        rez += "Омикронов\t\t::\t{}```".format(self.omicrons)

        if len(self.omicron_units) > 0:
            rez += "```==== Омикроны ====\n"
            for unit in self.omicron_units:
                rez += ("{}: Тир {}, {}⭐\n".format(unit[0], unit[2], unit[1]))
            rez += "```"

        rez += "```==== Арена ====\n"
        rez += "Лига: {}\n".format(self.ga_lyga)
        rez += "Отряд (Место - {}):\n".format(self.squadRank)
        rez += "Состав: {}\n".format(self.teamSquad)
        rez += "Флот (Место - {}):\n".format(self.flotRank)
        rez += "Флагман: {}\n".format(self.flotCapital)
        rez += "Стартовый состав: {}\n".format(self.flotStart)
        rez += "Подкрепление: {}```".format(self.flotReinforcement)

        rez += "```==== Флагманы ====\n"
        rez += "{}```".format(self.capitals)

        if len(self.toons1) > 0:
            rez += "```==== Одиночные Путешествия ====\n"
            for unit in self.toons1:
                rez += "{}: Тир {}, {}⭐\n".format(unit[0], unit[1], unit[2])
            rez += "```"

        if len(self.toons2) > 0:
            rez += "```==== Путешествие гильдий ====\n"
            for unit in self.toons2:
                rez += "{}: Тир {}, {}⭐\n".format(unit[0], unit[1], unit[2])
            rez += "```"

        if len(self.toons3) > 0:
            rez += "```==== Легенды ====\n"
            for unit in self.toons3:
                rez += "{}: Тир {}, {}⭐\n".format(unit[0], unit[1], unit[2])
            rez += "```"

        if len(self.toons4) > 0:
            rez += "```==== Завоевания ====\n"
            for unit in self.toons4:
                rez += "{}: Тир {}, {}⭐\n".format(unit[0], unit[1], unit[2])
            rez += "```"

        rez += "```==== Тиры ====\n"
        for gear in self.gears:
            if gear[1] > 0:
                rez += "{}\t::\t{}\n".format(gear[0], gear[1])
        rez += "```"

        rez += "```==== Моды ====\n"
        for mod in self.mods:
            if mod[2] > 0:
                rez += "{}\t::\t{}\n".format(mod[1], mod[2])
        rez += "```"

        return rez

    @staticmethod
    def compare(player):
        rez = ""
        names = []
        table = [
            ["Мощь \t\t", 0, 0],
            ["Топ 80 ГМ\t", 0, 0],
            ["Персонажи ГМ ", 0, 0],
            ["Флот ГМ  \t", 0, 0],
            ["Ранг на арене", 0, 0],
            ["Ранг на флоте", 0, 0]
        ]

        sep = "```"

        for i in range(0, len(player)):
            names.append(player[i].name)
            row = i + 1
            table[0][row] = player[i].allGM
            table[1][row] = player[i].top80gm
            table[2][row] = player[i].squadGm
            table[3][row] = player[i].flotGm
            table[4][row] = player[i].squadRank
            table[5][row] = player[i].flotRank

        rez += f"{sep}\n{names[0]} vs {names[1]}\n{sep}"
        rez += f"{sep}\n========== Обзор ==========\n"
        for line in table:
            rez += "{}\t::\t{}\tvs\t{}\n".format(line[0], line[1], line[2])
        rez += f"{sep}\n"

        table = []
        for i in range(len(player[0].gears)):
            add = [player[0].gears[i][0], player[0].gears[i][1], player[1].gears[i][1]]
            table.append(add)

        rez += f"{sep}\n========== Тиры ==========\n"
        for line in table:
            if line[1] > 0 or line[2] > 0:
                rez += "{}\t::\t{}\tvs\t{}\n".format(line[0], line[1], line[2])
        rez += f"{sep}\n"

        table = []
        for i in range(len(player[0].mods)):
            add = [player[0].mods[i][1], player[0].mods[i][2], player[1].mods[i][2]]
            table.append(add)

        rez += f"{sep}\n========== Моды ==========\n"
        for line in table:
            if line[1] > 0 or line[2] > 0:
                rez += "{}\t::\t{}\tvs\t{}\n".format(line[0], line[1], line[2])
        rez += f"{sep}\n"

        table = []
        for i in range(len(player[0].toons)):
            add = [player[0].toons[i][0], player[0].toons[i][1], player[0].toons[i][2], player[1].toons[i][1],
                   player[1].toons[i][2]]
            table.append(add)

        rez += f"{sep}\n========== Путешествия ==========\n"
        for line in table:
            if line[1] == line[3] == "Отсутствует":
                continue
            if line[1] == "Отсутствует":
                str = "Нет"
            else:
                str = "{} ГМ {}⭐".format(line[1], line[2])
            if line[3] == "Отсутствует":
                str2 = "Нет"
            else:
                str2 = "{} ГМ {}⭐".format(line[3], line[4])
            rez += "{}\n{}\tvs\t{}\n\n".format(line[0], str, str2)
        rez += f"{sep}\n"

        return rez
