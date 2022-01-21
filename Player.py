from api import api, settings
from func import *


class Player:
    @staticmethod
    def con():
        global auth
        global sw

        auth = settings('kudrin', '137235')
        sw = api(auth)

    def __init__(self, ally):
        self.con()

        payload = {'allycodes': ally, 'language': "RUS_RU", 'enums': True, 'project': {"name": 1,
                                                                                       "guildName": 1,
                                                                                       "stats": 1,
                                                                                       "roster": 1,
                                                                                       "arena": 1,
                                                                                       "grandArena": 1
                                                                                       }}
        player = sw.fetchPlayers(payload)
        player = player[0]

        self.name = player['name']
        self.guildName = player['guildName']
        self.allGM = player['stats'][0]['value']
        self.squadGm = player['stats'][1]['value']
        self.flotGm = player['stats'][2]['value']
        self.zetas, self.omicrons, self.omicron_units = func.get_zeta_omicron(sw, player['roster'])

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
        print("==== Обзор ====")
        print("\tНикнейм (Гильдия):\t\t{} ({})".format(self.name, self.guildName))
        print("\tМощь:\t\t\t\t\t{}".format(self.allGM))
        print("\tПерсонажи ГМ:\t\t\t{}".format(self.squadGm))
        print("\tФлот ГМ:\t\t\t\t{}".format(self.flotGm))
        print("\tДзет:\t\t\t\t\t{}".format(self.zetas))
        print("\tОмикронов:\t\t\t\t{}".format(self.omicrons))
        print()

        if len(self.omicron_units) > 0:
            print("==== Омикроны ====")
            for unit in self.omicron_units:
                print("{}: Тир {}, {}⭐".format(unit[0],unit[2], unit[1]))
            print()

        print("==== Арена ====")
        print("Лига: {}".format(self.ga_lyga))
        print("Отряд (Место - {}):".format(self.squadRank))
        print("\tСостав:\t\t\t\t\t{}".format(self.teamSquad))
        print("Флот (Место - {}):".format(self.flotRank))
        print("\tФлагман:\t\t\t\t{}".format(self.flotCapital))
        print("\tСтартовый состав:\t\t{}".format(self.flotStart))
        print("\tПодкрепление:\t\t\t{}".format(self.flotReinforcement))
        print()

        print("==== Флагманы ====")
        print("{}".format(self.capitals))
        print()

        if len(self.toons) > 0:
            print("==== Одиночные Путешествия ====")
            for unit in self.toons:
                print("\t{}: Тир {}, {}⭐".format(unit[0], unit[1], unit[2]))
            print()

        if len(self.toons2) > 0:
            print("==== Путешествие гильдий ====")
            for unit in self.toons2:
                print("\t{}: Тир {}, {}⭐".format(unit[0], unit[1], unit[2]))
            print()

        if len(self.toons3) > 0:
            print("==== Легенды ====")
            for unit in self.toons3:
                print("\t{}: Тир {}, {}⭐".format(unit[0], unit[1], unit[2]))
            print()

        if len(self.toons4) > 0:
            print("==== Завоевания ====")
            for unit in self.toons4:
                print("\t{}: Тир {}, {}⭐".format(unit[0], unit[1], unit[2]))
            print()

        print("==== Тиры ====")
        for gear in self.gears:
            if gear[1] > 0:
                print("{}: {}".format(gear[0], gear[1]))
        print()

        print("==== Моды ====")
        for mod in self.mods:
            if mod[2] > 0:
                print("{}: {}".format(mod[1], mod[2]))
