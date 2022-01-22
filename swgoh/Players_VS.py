from swgoh.func import *


class Players_VS:
    def __init__(self, ally):
        player = func.get_info(ally)

        self.name = player['name']
        self.allGM = player['stats'][0]['value']
        self.top80gm = self.get_top80(player['roster'])
        self.squadGm = player['stats'][1]['value']
        self.flotGm = player['stats'][2]['value']
        self.squadRank = player['arena']['char']['rank']
        self.flotRank = player['arena']['ship']['rank']

        self.gears = func.get_gears(player['roster'])

        self.mods = func.get_mods(player['roster'])

        self.toons = self.get_toons(player['roster'])

    @staticmethod
    def write(player):
        rez = ""
        names = []
        table = [
            ["Мощь\t\t", 0, 0],
            ["Топ 80 ГМ\t", 0, 0],
            ["Персонажи ГМ", 0, 0],
            ["Флот ГМ\t", 0, 0],
            ["Ранг на арене", 0, 0],
            ["Ранг на флоте", 0, 0]
        ]

        for i in range(0, len(player)):
            names.append(player[i].name)
            row = i + 1
            table[0][row] = player[i].allGM
            table[1][row] = player[i].top80gm
            table[2][row] = player[i].squadGm
            table[3][row] = player[i].flotGm
            table[4][row] = player[i].squadRank
            table[5][row] = player[i].flotRank

        rez += "```{} vs {}```".format(names[0], names[1])
        rez += "```========== Обзор ==========\n"
        for line in table:
            rez += "{}\n\t{}\tvs\t{}\n".format(line[0], line[1], line[2])
        rez += "```"

        table = []
        for i in range(len(player[0].gears)):
            add = [player[0].gears[i][0], player[0].gears[i][1], player[1].gears[i][1]]
            table.append(add)

        rez += "```========== Тиры ==========\n"
        for line in table:
            if line[1] > 0 or line[2] > 0:
                rez += "{}\n\t{}\tvs\t{}\n".format(line[0], line[1], line[2])
        rez += "```"

        table = []
        for i in range(len(player[0].mods)):
            add = [player[0].mods[i][1], player[0].mods[i][2], player[1].mods[i][2]]
            table.append(add)

        rez += "```========== Моды ==========\n"
        for line in table:
            if line[1] > 0 or line[2] > 0:
                rez += "{}\n\t{}\tvs\t{}\n".format(line[0], line[1], line[2])
        rez += "```"

        table = []
        for i in range(len(player[0].toons)):
            add = [player[0].toons[i][0], player[0].toons[i][1], player[0].toons[i][2], player[1].toons[i][1],
                   player[1].toons[i][2]]
            table.append(add)

        rez += "```========== Путешествия ==========\n"
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
            rez += "{}\n\t{}\tvs\t{}\n\n".format(line[0], str, str2)
        rez += "```"

        return rez

    @staticmethod
    def get_toons(units):
        list = ["Падме Амидала", "Старкиллер", "Рыцарь-джедай Реван", "Дарт Реван", "Дарт Малак", "Генерал Скайуокер",
                "Рыцарь-джедай Люк Скайуокер", "Ват Тамбор", "Ки-Ади-Мунди", "Лорд Вейдер", "Мастер-джедай Кеноби",
                "Мастер-джедай Люк Скайуокер", "Император Вечных ситхов",
                "Верховный лидер Кайло Рен", "Рей", "Командир Асока Тано", "Мол", "Боба Фет (потомок джанго)", "Палач"]

        rez = []
        for chech_unit in list:
            added = False
            for unit in units:
                if unit['nameKey'] == chech_unit:
                    el = [chech_unit, unit['gp'], unit['rarity']]
                    rez.append(el)
                    added = True
            if not added:
                el = [chech_unit, "Отсутствует", 0]
                rez.append(el)

        return rez

    @staticmethod
    def get_top80(units):
        list = []

        for unit in units:
            if unit['combatType'] == 'CHARACTER':
                list.append(unit['gp'])

        list.sort(reverse=True)

        sum_gp = 0
        for i in range(0, len(list)):
            sum_gp += list[i]

        return sum_gp
