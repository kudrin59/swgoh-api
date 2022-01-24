from swgoh.func import *


class Player:
    def __init__(self, ally):
        player = func.get_player(ally)

        self.name = player['name']
        print(f"Запрошена информация об игроке: {self.name}")
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

    def write_pc(self):
        data = []

        title = ""
        value = ""

        title += "Ник (Гильдия)\n"
        value += "{} ({})\n".format(self.name, self.guildName)
        title += "Мощь\n"
        value += "{}\n".format(self.allGM)
        title += "Персонажи ГМ\n"
        value += "{}\n".format(self.squadGm)
        title += "Флот ГМ\n"
        value += "{}\n".format(self.flotGm)
        title += "Дзет\n"
        value += "{}\n".format(self.zetas)
        title += "Омикронов\n"
        value += "{}\n".format(self.omicrons)
        data.append(['= Обзор =', title, value])

        if self.omicrons > 0:
            title = ""
            value = ""
            for unit in self.omicron_units:
                title += unit[0]
                value += ("Тир {}, {}⭐\n".format(unit[0], unit[2], unit[1]))
            data.append(['= Омикроны =', title, value])

        title = ""
        value = ""
        title += "Лига:\n"
        value += "{}\n".format(self.ga_lyga)
        title += "Место отряда:\n"
        value += "{}\n".format(self.squadRank)
        # title += "Состав:\n"
        # value += "{}\n".format(self.teamSquad)
        title += "Место флота:\n"
        value += "{}\n".format(self.flotRank)
        # title += "Флагман:\n"
        # value += "{}\n".format(self.flotCapital)
        # title += "Стартовый состав:\n"
        # value += "{}\n".format(self.flotStart)
        # title += "Подкрепление:\n"
        # value += "{}\n".format(self.flotReinforcement)
        data.append(['= Арена =', title, value])

        if len(self.capitals) > 0:
            title = "= Флагманы ="
            value = self.capitals
            data.append([title, value])

        if len(self.toons1) > 0:
            title = ""
            value = ""
            for unit in self.toons1:
                title += "{}\n".format(unit[0])
                value += "Тир {}, {}⭐\n".format(unit[1], unit[2])
            data.append(['= Одиночные Путешествия =', title, value])

        if len(self.toons2) > 0:
            title = ""
            value = ""
            for unit in self.toons2:
                title += "{}\n".format(unit[0])
                value += "Тир {}, {}⭐\n".format(unit[1], unit[2])
            data.append(['= Путешествия Гильдий =', title, value])

        if len(self.toons3) > 0:
            title = ""
            value = ""
            for unit in self.toons3:
                title += "{}\n".format(unit[0])
                value += "Тир {}, {}⭐\n".format(unit[1], unit[2])
            data.append(['= Легенды =', title, value])

        if len(self.toons4) > 0:
            title = ""
            value = ""
            for unit in self.toons4:
                title += "{}\n".format(unit[0])
                value += "Тир {}, {}⭐\n".format(unit[1], unit[2])
            data.append(['= Завоевания =', title, value])

        if len(self.gears) > 0:
            title = ""
            value = ""
            for gear in self.gears:
                if gear[1] > 0:
                    title += "{}\n".format(gear[0])
                    value += "{}\n".format(gear[1])
            data.append(['= Тиры =', title, value])

        if len(self.mods) > 0:
            title = ""
            value = ""
            for mod in self.mods:
                if mod[2] > 0:
                    title += "{}\n".format(mod[1])
                    value += "{}\n".format(mod[2])
            data.append(['= Моды =', title, value])

        return self.name, data

    def write_phone(self):
        data = []

        rez = "Ник (Гильдия) : {} ({})\n".format(self.name, self.guildName)
        rez += "Мощь : {}\n".format(self.allGM)
        rez += "Персонажи ГМ : {}\n".format(self.squadGm)
        rez += "Флот ГМ : {}\n".format(self.flotGm)
        rez += "Дзет : {}\n".format(self.zetas)
        rez += "Омикронов : {}\n".format(self.omicrons)
        data.append(['= Обзор =', rez])

        if self.omicrons > 0:
            rez = ""
            for unit in self.omicron_units:
                rez += unit[0]
                rez += ("Тир {}, {}⭐\n".format(unit[0], unit[2], unit[1]))
            data.append(['= Омикроны =', rez])

        rez = "Лига : {}\n".format(self.ga_lyga)
        rez += "Место отряда : {}\n".format(self.squadRank)
        rez += "Место флота : {}\n".format(self.flotRank)
        data.append(['= Арена =', rez])

        if len(self.capitals) > 0:
            rez = self.capitals
            data.append(["= Флагманы =", rez])

        if len(self.toons1) > 0:
            rez = ""
            for unit in self.toons1:
                rez += "{} : Тир {}, {}⭐\n".format(unit[0], unit[1], unit[2])
            data.append(['= Одиночные Путешествия =', rez])

        if len(self.toons2) > 0:
            rez = ""
            for unit in self.toons2:
                rez += "{} : Тир {}, {}⭐\n".format(unit[0], unit[1], unit[2])
            data.append(['= Путешествия Гильдий =', rez])

        if len(self.toons3) > 0:
            rez = ""
            for unit in self.toons3:
                rez += "{} : Тир {}, {}⭐\n".format(unit[0], unit[1], unit[2])
            data.append(['= Легенды =', rez])

        if len(self.toons4) > 0:
            rez = ""
            for unit in self.toons4:
                rez += "{} : Тир {}, {}⭐\n".format(unit[0], unit[1], unit[2])
            data.append(['= Завоевания =', rez])

        if len(self.gears) > 0:
            rez = ""
            for gear in self.gears:
                if gear[1] > 0:
                    rez += "{} : {}\n".format(gear[0], gear[1])
            data.append(['= Тиры =', rez])

        if len(self.mods) > 0:
            rez = ""
            for mod in self.mods:
                if mod[2] > 0:
                    rez += "{} : {}\n".format(mod[1], mod[2])
            data.append(['= Моды =', rez])

        return self.name, data

    @staticmethod
    def compare_pc(player):
        data = []

        table = [
            ["Мощь", 0, 0],
            ["Топ 80 ГМ", 0, 0],
            ["Персонажи ГМ ", 0, 0],
            ["Флот ГМ", 0, 0],
            ["Ранг на арене", 0, 0],
            ["Ранг на флоте", 0, 0]
        ]

        for i in range(0, len(player)):
            row = i + 1
            table[0][row] = player[i].allGM
            table[1][row] = player[i].top80gm
            table[2][row] = player[i].squadGm
            table[3][row] = player[i].flotGm
            table[4][row] = player[i].squadRank
            table[5][row] = player[i].flotRank

        title = ""
        rez_player = ""
        rez_player2 = ""
        for line in table:
            title += "{}\n".format(line[0])
            rez_player += "{}\n".format(line[1])
            rez_player2 += "{}\n".format(line[2])
        data.append(['= Обзор =', title, rez_player, rez_player2])

        table = []
        for i in range(len(player[0].gears)):
            add = [player[0].gears[i][0], player[0].gears[i][1], player[1].gears[i][1]]
            table.append(add)

        title = ""
        rez_player = ""
        rez_player2 = ""
        for line in table:
            if line[1] > 0 or line[2] > 0:
                title += "{}\n".format(line[0])
                rez_player += "{}\n".format(line[1])
                rez_player2 += "{}\n".format(line[2])
        data.append(['= Тиры =', title, rez_player, rez_player2])

        table = []
        for i in range(len(player[0].mods)):
            add = [player[0].mods[i][1], player[0].mods[i][2], player[1].mods[i][2]]
            table.append(add)

        title = ""
        rez_player = ""
        rez_player2 = ""
        for line in table:
            if line[1] > 0 or line[2] > 0:
                title += "{}\n".format(line[0])
                rez_player += "{}\n".format(line[1])
                rez_player2 += "{}\n".format(line[2])
        data.append(['= Моды =', title, rez_player, rez_player2])

        table = []
        for i in range(len(player[0].toons)):
            add = [player[0].toons[i][0], player[0].toons[i][1], player[0].toons[i][2], player[1].toons[i][1],
                   player[1].toons[i][2]]
            table.append(add)

        title = ""
        rez_player = ""
        rez_player2 = ""
        for line in table:
            if line[1] == line[3] == "Отсутствует":
                continue
            if line[1] == "Отсутствует":
                temp_str = "Нет"
            else:
                temp_str = "{} ГМ {}⭐".format(line[1], line[2])
            if line[3] == "Отсутствует":
                temp_str_2 = "Нет"
            else:
                temp_str_2 = "{} ГМ {}⭐".format(line[3], line[4])
            title += "{}\n".format(line[0])
            rez_player += "{}\n".format(temp_str)
            rez_player2 += "{}\n".format(temp_str_2)
        data.append(['= Путешествия =', title, rez_player, rez_player2])

        player_name = [player[0].name, player[1].name]

        return player_name, data

    @staticmethod
    def compare_phone(player):
        data = []

        table = [
            ["Мощь", 0, 0],
            ["Топ 80 ГМ", 0, 0],
            ["Персонажи ГМ", 0, 0],
            ["Флот ГМ", 0, 0],
            ["Ранг на арене", 0, 0],
            ["Ранг на флоте", 0, 0]
        ]

        for i in range(0, len(player)):
            row = i + 1
            table[0][row] = player[i].allGM
            table[1][row] = player[i].top80gm
            table[2][row] = player[i].squadGm
            table[3][row] = player[i].flotGm
            table[4][row] = player[i].squadRank
            table[5][row] = player[i].flotRank

        rez = ""
        for line in table:
            rez += "{}: {} vs {}\n".format(line[0], line[1], line[2])
        data.append(["= Обзор =", rez])

        table = []
        for i in range(len(player[0].gears)):
            add = [player[0].gears[i][0], player[0].gears[i][1], player[1].gears[i][1]]
            table.append(add)

        rez = ""
        for line in table:
            if line[1] > 0 or line[2] > 0:
                rez += "{} : {} vs {}\n".format(line[0], line[1], line[2])
        data.append(["= Тиры =", rez])

        table = []
        for i in range(len(player[0].mods)):
            add = [player[0].mods[i][1], player[0].mods[i][2], player[1].mods[i][2]]
            table.append(add)

        rez = ""
        for line in table:
            if line[1] > 0 or line[2] > 0:
                rez += "{} : {} vs {}\n".format(line[0], line[1], line[2])
        data.append(["= Моды =", rez])

        table = []
        for i in range(len(player[0].toons)):
            add = [player[0].toons[i][0], player[0].toons[i][1], player[0].toons[i][2], player[1].toons[i][1],
                   player[1].toons[i][2]]
            table.append(add)

        rez = ""
        for line in table:
            if line[1] == line[3] == "Отсутствует":
                continue
            if line[1] == "Отсутствует":
                temp_str = "Нет"
            else:
                temp_str = "{} ГМ {}⭐".format(line[1], line[2])
            if line[3] == "Отсутствует":
                temp_str_2 = "Нет"
            else:
                temp_str_2 = "{} ГМ {}⭐".format(line[3], line[4])
            rez += "{}\n\t{} vs {}\n".format(line[0], temp_str, temp_str_2)
        data.append(["= Путешествия =", rez])

        player_name = [player[0].name, player[1].name]

        return player_name, data
