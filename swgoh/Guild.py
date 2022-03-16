from swgoh.func import *


class Guild:
    def __init__(self, ally):
        self.name, self.members, self.gm, players_ally = self.get_users_guild(ally)
        print(f"Запрошена информация о гильии: {self.name}")
        users_data = self.get_users_info(players_ally)
        self.zetas, self.omicrons, self.count_omicrons = self.get_zeta_omicron(users_data)
        self.toons = self.get_toons(users_data)
        self.count_legs = self.get_count_unit(self.toons)

    def info(self):
        return self.name, self.info_form()

    def info_form(self):
        data = []
        data = self.g_obzor(data)
        data = self.g_legs(data)
        data = self.g_omicrons(data)
        return data

    def g_obzor(self, data):
        temp = []
        temp.append(['ГМ', self.gm])
        temp.append(['Игроков ГМ', self.members])
        temp.append(['Дзет', self.zetas])
        temp.append(['Омикронов', self.omicrons])
        data.append(['=== Обзор ===', temp])
        return data

    def g_legs(self, data):
        if len(self.count_legs) > 0:
            temp = []
            for unit in self.count_legs:
                temp.append([unit[0], unit[1]])
            data.append(['=== Легенды ===', temp])
        return data

    def g_omicrons(self, data):
        if len(self.count_omicrons) > 0:
            temp = []
            for unit in self.count_omicrons:
                temp.append([unit[0], unit[1]])
            data.append(['=== Омикроны ===', temp])
        return data

    @staticmethod
    def get_toons(users_data):
        toons = []
        for player in users_data:
            temp_toons, temp_toons2, temp_toons3, temp_toons4 = func.get_toons(player['roster'])
            toons.append(temp_toons3)
        return toons

    @staticmethod
    def get_count_unit(toons):
        list = []
        for user in toons:
            for unit in user:
                add = False
                for leg in list:
                    if leg[0] == unit[0]:
                        leg[1] += 1
                        add = True
                        break
                if not add:
                    list.append([unit[0], 1])
        return list

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
        omicron_units = []

        for player in users_data:
            for unit in player['roster']:
                for skill in unit['skills']:
                    if skill['id'] in omicron_skills:
                        if skill['isZeta']:
                            if skill['tier'] == skill['tiers']:
                                omicrons += 1
                                omicron_units.append(unit['nameKey'])
                                zetas += 1
                            elif skill['tier'] == skill['tiers'] - 1:
                                zetas += 1
                        else:
                            if skill['tier'] == skill['tiers']:
                                omicrons += 1
                                omicron_units.append(unit['nameKey'])
                    else:
                        if skill['tier'] == skill['tiers'] and skill['isZeta']:
                            zetas += 1

        count_omicrons = Guild.get_count_omicrons(omicron_units)

        return zetas, omicrons, count_omicrons

    @staticmethod
    def get_count_omicrons(units):
        list = []
        for unit in units:
            add = False
            for charter in list:
                if charter[0] == unit:
                    charter[1] += 1
                    add = True
                    break
            if not add:
                list.append([unit, 1])
        return list

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
