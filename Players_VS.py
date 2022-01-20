from api import api, settings


class Players_VS:
    @staticmethod
    def con():
        global auth
        global sw

        auth = settings('kudrin', '137235')
        sw = api(auth)

    def __init__(self, ally):
        self.con()

        payload = {'allycodes': ally, 'language': "RUS_RU", 'enums': True, 'project': {"name": 1,
                                                                                       "stats": 1
                                                                                       }}
        player = sw.fetchPlayers(payload)
        player = player[0]

        self.name = player['name']
        self.allGM = player['stats'][0]['value']
        self.squadGm = player['stats'][1]['value']
        self.flotGm = player['stats'][2]['value']

    @staticmethod
    def write(player):
        names = []
        table = [
            ["========= Обзор =========", True],
            ["Мощь\t\t", 0, 0],
            ["Персонажи ГМ", 0, 0],
            ["Флот ГМ\t\t", 0, 0]
        ]

        for i in range(len(player)):
            names.append(player[i].name)
            row = i + 1
            table[1][row] = player[i].allGM
            table[2][row] = player[i].squadGm
            table[3][row] = player[i].flotGm

        print("{0} vs {1}".format(names[0], names[1]))
        for line in table:
            if line[1] == True:
                print(line[0])
            else:
                print("{0}\t::\t{1}\tvs\t{2}".format(line[0], line[1], line[2]))
        print()
