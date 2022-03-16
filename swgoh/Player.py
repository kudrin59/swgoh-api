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

        self.units = player['roster']

    def info(self):
        return self.name, self.info_form()

    def info_form(self):
        data = []
        data = self.p_obzor(data)
        data = self.p_omicrons(data)
        data = self.p_arena(data)
        data = self.p_flagmans(data)
        data = self.p_gears(data)
        data = self.p_mods(data)
        data = self.p_toons1(data)
        data = self.p_toons2(data)
        data = self.p_toons3(data)
        data = self.p_toons4(data)
        return data

    def p_obzor(self, data):
        temp = []
        temp.append(['Ник (Гильдия)', f'{self.name} ({self.guildName})'])
        temp.append(['Мощь', self.allGM])
        temp.append(['Персонажи ГМ', self.squadGm])
        temp.append(['Флот ГМ', self.flotGm])
        temp.append(['Дзет', self.zetas])
        temp.append(['Омикронов', self.omicrons])
        data.append(['=== Обзор ===', temp])
        return data

    def p_omicrons(self, data):
        if self.omicrons > 0:
            temp = []
            for unit in self.omicron_units:
                temp.append([unit[0], f'Тир {unit[2]}, {unit[1]}⭐'])
            data.append(['=== Омикроны ===', temp])
        return data

    def p_arena(self, data):
        temp = []
        temp.append(['Лига', self.ga_lyga])
        temp.append(['Место отряда', self.squadRank])
        # temp.append(['Состав', self.teamSquad])
        temp.append(['Место флота', self.flotRank])
        temp.append(['Флагман', self.flotCapital])
        # temp.append(['Стартовый состав', self.flotStart])
        # temp.append(['Подкрепление', self.flotReinforcement])
        data.append(['=== Арена ===', temp])
        return data

    def p_flagmans(self, data):
        if len(self.capitals) > 0:
            temp = []
            for capital in self.capitals:
                temp.append([capital[0], f'{capital[1]} ⭐'])
            data.append(['=== Флагманы ===', temp])
        return data

    def p_gears(self, data):
        if len(self.gears) > 0:
            temp = []
            for gear in self.gears:
                if gear[1] > 0:
                    temp.append([gear[0], gear[1]])
            data.append(['=== Тиры ===', temp])
        return data

    def p_mods(self, data):
        if len(self.mods) > 0:
            temp = []
            for mod in self.mods:
                if mod[2] > 0:
                    temp.append([mod[1], mod[2]])
            data.append(['=== Моды ===', temp])
        return data

    def p_toons1(self, data):
        if len(self.toons1) > 0:
            temp = []
            for unit in self.toons1:
                temp.append([unit[0], f'Тир {unit[1]}, {unit[2]}⭐'])
            data.append(['=== Одиночные Путешествия ===', temp])
        return data

    def p_toons2(self, data):
        if len(self.toons2) > 0:
            temp = []
            for unit in self.toons2:
                temp.append([unit[0], f'Тир {unit[1]}, {unit[2]}⭐'])
            data.append(['=== Путешествия Гильдий ===', temp])
        return data

    def p_toons3(self, data):
        if len(self.toons3) > 0:
            temp = []
            for unit in self.toons3:
                temp.append([unit[0], f'Тир {unit[1]}, {unit[2]}⭐'])
            data.append(['=== Легенды ===', temp])
        return data

    def p_toons4(self, data):
        if len(self.toons4) > 0:
            temp = []
            for unit in self.toons4:
                temp.append([unit[0], f'Тир {unit[1]}, {unit[2]}⭐'])
            data.append(['=== Завоевания ===', temp])
        return data

    @staticmethod
    def compare(players):
        return Player.compare_form(players)

    @staticmethod
    def compare_form(players):
        data = []
        data = Player.compare_obzor(players, data)
        data = Player.compare_gears(players, data)
        data = Player.compare_mods(players, data)
        data = Player.compare_toons(players, data)

        players_name = [players[0].name, players[1].name]
        return players_name, data

    @staticmethod
    def compare_obzor(players, data):
        temp = []
        temp.append(['Мощь', players[0].allGM, players[1].allGM])
        temp.append(['Персонажи ГМ', players[0].squadGm, players[1].squadGm])
        temp.append(['Флот ГМ', players[0].flotGm, players[1].flotGm])
        temp.append(['Дзет', players[0].zetas, players[1].zetas])
        temp.append(['Омикронов', players[0].omicrons, players[1].omicrons])
        data.append(['=== Обзор ===', temp])
        return data

    @staticmethod
    def compare_gears(players, data):
        temp = []
        for i in range(len(players[0].gears)):
            if players[0].gears[i][1] > 0 or players[1].gears[i][1] > 0:
                temp.append([players[0].gears[i][0], players[0].gears[i][1], players[1].gears[i][1]])
        data.append(["=== Тиры ===", temp])
        return data

    @staticmethod
    def compare_mods(players, data):
        temp = []
        for i in range(len(players[0].mods)):
            if players[0].mods[i][2] > 0 or players[1].mods[i][2] > 0:
                temp.append([players[0].mods[i][1], players[0].mods[i][2], players[1].mods[i][2]])
        data.append(["=== Моды ===", temp])
        return data

    @staticmethod
    def compare_toons(players, data):
        temp = []
        for i in range(len(players[0].toons)):
            if players[0].toons[i][2] > 0 or players[1].toons[i][2] > 0:
                if players[0].toons[i][1] != "Отсутствует":
                    temp_str = f'{players[0].toons[i][1]} ГМ {players[0].toons[i][2]}⭐'
                else:
                    temp_str = players[0].toons[i][1]
                if players[1].toons[i][1] != "Отсутствует":
                    temp_str_2 = f'{players[1].toons[i][1]} ГМ {players[1].toons[i][2]}⭐'
                else:
                    temp_str_2 = players[1].toons[i][1]
                temp.append([players[0].toons[i][0], temp_str, temp_str_2])
        data.append(["=== Путешествия ===", temp])
        return data
