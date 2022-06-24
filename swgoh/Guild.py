from swgoh.func import *


class Guild:
    def __init__(self, ally):
        self.name, self.members, self.gm, players_ally = self.get_users_guild(ally)
        users_data = self.get_users_info(players_ally)
        self.zetas, self.omicrons, self.count_omicrons = self.get_zeta_omicron(users_data)
        self.toons = self.get_toons(users_data)
        self.count_legs = self.get_count_unit(self.toons)
        self.mods = self.get_mods(users_data)
        self.gears = self.get_gears(users_data)

    def info(self):
        return self.name, self.info_form()

    def info_form(self):
        data = []
        data = self.g_obzor(data)
        data = self.g_legs(data)
        data = self.g_omicrons(data)
        data = self.g_mods(data)
        data = self.g_gears(data)
        return data

    def g_obzor(self, data):
        temp = []
        temp.append(['ГМ', self.gm])
        temp.append(['Игроков', self.members])
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

    def g_mods(self, data):
        if len(self.mods) > 0:
            temp = []
            for mod in self.mods:
                if mod[2] > 0:
                    temp.append([mod[1], mod[2]])
            data.append(['=== Моды ===', temp])
        return data

    def g_gears(self, data):
        if len(self.gears) > 0:
            temp = []
            for gear in self.gears:
                if gear[1] > 0:
                    temp.append([gear[0], gear[1]])
            data.append(['=== Тиры ===', temp])
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
    def get_mods(users_data):
        rez = [["pips", "МК6", 0, 6], ["UNITSTATSPEED", "Скорость 15+", 0, 15],
               ["UNITSTATSPEED", "Скорость 20+", 0, 20], ["UNITSTATSPEED", "Скорость 25+", 0, 25]]
        max_speed = 999
        for player in users_data:
            for unit in player['roster']:
                for mod in unit['mods']:
                    if mod['pips'] >= rez[0][3]:
                        rez[0][2] += 1
                    for stat in mod['secondaryStat']:
                        for i in range(1, len(rez)):
                            if i == len(rez) - 1:
                                next_value = max_speed
                            else:
                                next_value = rez[i + 1][3]
                            if (stat['unitStat'] == rez[i][0]) and (stat['value'] >= rez[i][3]) and (
                                    stat['value'] < next_value):
                                rez[i][2] += 1

        return rez

    @staticmethod
    def get_gears(users_data):
        # Название, Количество, От какого рела, До какого рела
        rez = [["Т13", 0, 0, 9], ["Р1-4", 0, 1, 4], ["Р5", 0, 5, 5], ["Р6", 0, 6, 6], ["Р7", 0, 7, 7],
               ["Р8", 0, 8, 8],
               ["Р9", 0, 9, 9]]
        for player in users_data:
            for unit in player['roster']:
                if unit['combatType'] == 'CHARACTER':
                    for gear in rez:
                        rel = unit['relic']['currentTier'] - 2
                        if (rel >= gear[2]) and (rel <= gear[3]):
                            gear[1] += 1
        return rez

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

    @staticmethod
    def compare(guilds):
        return Guild.compare_form(guilds)

    @staticmethod
    def compare_form(guilds):
        data = []
        data = Guild.compare_obzor(guilds, data)
        data = Guild.compare_gears(guilds, data)
        data = Guild.compare_mods(guilds, data)

        guilds_name = [guilds[0].name, guilds[1].name]
        return guilds_name, data

    @staticmethod
    def compare_obzor(guilds, data):
        temp = []
        temp.append(['ГМ', guilds[0].gm, guilds[1].gm])
        temp.append(['Персонажи', guilds[0].members, guilds[1].members])
        temp.append(['Дзет', guilds[0].zetas, guilds[1].zetas])
        temp.append(['Омикронов', guilds[0].omicrons, guilds[1].omicrons])
        data.append(['=== Обзор ===', temp])
        return data

    @staticmethod
    def compare_gears(guilds, data):
        temp = []
        for i in range(len(guilds[0].gears)):
            if guilds[0].gears[i][1] > 0 or guilds[1].gears[i][1] > 0:
                temp.append([guilds[0].gears[i][0], guilds[0].gears[i][1], guilds[1].gears[i][1]])
        data.append(["=== Тиры ===", temp])
        return data

    @staticmethod
    def compare_mods(guilds, data):
        temp = []
        for i in range(len(guilds[0].mods)):
            if guilds[0].mods[i][2] > 0 or guilds[1].mods[i][2] > 0:
                temp.append([guilds[0].mods[i][1], guilds[0].mods[i][2], guilds[1].mods[i][2]])
        data.append(["=== Моды ===", temp])
        return data
