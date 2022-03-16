from swgoh.func import *


class Guild:
    def __init__(self, ally):
        self.name, self.members, self.gm, players_ally = self.get_users_guild(ally)
        print(f"Запрошена информация о гильии: {self.name}")

        users_data = self.get_users_info(players_ally)
        self.zetas, self.omicrons = self.get_zeta_omicron(users_data)
        print(f"ГМ: {self.gm}")
        print(f"Игроков: {self.members}")
        print(f"Дзет: {self.zetas}")
        print(f"Омикронов: {self.omicrons}")

    @staticmethod
    def get_zeta_omicron(users_data):
        sw = func.con()

        payload = {}
        payload['collection'] = "skillList"
        payload['language'] = "rus_ru"
        payload['enums'] = True
        payload['project'] = {"id": 1,
                              "abilityReference": 1,
                              "isZeta": 1,
                              'tierList': 1
                              }
        items = sw.fetchData(payload)

        skills = {}
        for skill in items:
            skills[skill['id']] = skill
            omicrons = [tl['recipeId'] for tl in skill['tierList'] if "OMICRON" in tl['recipeId']]
            skills[skill['id']]['isOmicron'] = True if omicrons else False

        omicron_skills = [skill for skill in skills if skills[skill]['isOmicron']]

        zetas = 0
        omicrons = 0

        for player in users_data:
            for unit in player['roster']:
                for skill in unit['skills']:
                    if skill['isZeta']:
                        if skill['id'] in omicron_skills:
                            if skill['tier'] == skill['tiers']:
                                omicrons += 1
                                zetas += 1
                            elif skill['tier'] == skill['tiers'] - 1:
                                zetas += 1
                        else:
                            if skill['tier'] == skill['tiers']:
                                zetas += 1

        return zetas, omicrons

    @staticmethod
    def get_users_info(allys):
        sw = func.con()

        payload = {}
        payload['allycodes'] = allys
        payload['language'] = "rus_ru"
        payload['enums'] = True
        payload['project'] = {"name": 1,
                              "stats": 1,
                              "roster": 1,
                              "arena": 1,
                              'grandArena': 1
                              }

        data = sw.fetchPlayers(payload)

        return data

    @staticmethod
    def get_users_guild(guild):
        sw = func.con()

        payload = {}
        payload['allycodes'] = guild
        payload['language'] = "rus_ru"
        payload['enums'] = True

        data = sw.fetchGuilds(payload)

        name = data[0]['name']  # Название гильии
        members = data[0]['members']  # Количество игроков
        gm = data[0]['gp']  # Количество гм
        data = data[0]['roster']  # Информация об игроках

        users = []
        for user in data:
            users.append(user['allyCode'])

        return name, members, gm, users
