from swgoh.func import *


class Player:
    def __init__(self, ally):
        player = func.get_info(ally)

        self.name = player['name']
        self.guildName = player['guildName']
        self.allGM = player['stats'][0]['value']
        self.squadGm = player['stats'][1]['value']
        self.flotGm = player['stats'][2]['value']
        self.zetas, self.omicrons, self.omicron_units = func.get_zeta_omicron(player['roster'])

        self.ga_lyga = func.get_ga(player['grandArena'])

        self.squadRank = player['arena']['char']['rank']
        self.teamSquad = func.get_arena_squad(player)

        self.flotRank = player['arena']['ship']['rank']
        self.flotCapital, self.flotStart, self.flotReinforcement = func.get_arena_ship(player)

        self.capitals = func.get_capitals(player['roster'])

        self.toons, self.toons2, self.toons3, self.toons4 = func.get_toons(player['roster'])

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

        if len(self.toons) > 0:
            rez += "```==== Одиночные Путешествия ====\n"
            for unit in self.toons:
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
