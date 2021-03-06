from swgoh.api import *


class func:
    @staticmethod
    def con():
        date = open('swgoh_help.txt', 'r').readline().split(";")
        user_login = date[0]
        user_pass = date[1]

        auth = settings(user_login, user_pass)
        sw = api(auth)
        return sw

    @staticmethod
    def get_toons_compare(units):
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

    @staticmethod
    def get_player(ally):
        sw = func.con()

        payload = {}
        payload['allycodes'] = ally
        payload['language'] = "rus_ru"
        payload['enums'] = True
        payload['project'] = {"name": 1,
                              "guildName": 1,
                              "stats": 1,
                              "roster": 1,
                              "arena": 1,
                              'grandArena': 1
                              }

        player = sw.fetchPlayers(payload)

        return player[0]

    @staticmethod
    def get_ga(seasons):
        divisions = {
            5: 5,
            10: 4,
            15: 3,
            20: 2,
            25: 1
        }

        leagues = {
            "CARBONITE": "Карбонитовая",
            "BRONZIUM": "Бронзиумная",
            "CHROMIUM": "Хромиумная",
            "AURODIUM": "Ауродиумная",
            "KYBER": "Кайбер"
        }

        season = seasons[len(seasons) - 1]

        league = leagues[season['league']]
        division = divisions[season['division']]
        rank = season['rank']

        rez = "{} {}, ранг - {}".format(league, division, rank)

        return rez

    @staticmethod
    def get_mods(units):
        rez = [["pips", "МК6", 0, 6], ["UNITSTATSPEED", "Скорость 15+", 0, 15],
               ["UNITSTATSPEED", "Скорость 20+", 0, 20], ["UNITSTATSPEED", "Скорость 25+", 0, 25]]
        max_speed = 999

        for unit in units:
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
    def get_zeta_omicron(units):
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

        for unit in units:
            for skill in unit['skills']:
                if skill['id'] in omicron_skills:
                    if skill['isZeta']:
                        if skill['tier'] == skill['tiers']:
                            omicrons += 1
                            temp_unit = [unit['nameKey'], unit['rarity'], unit['gear']]
                            omicron_units.append(temp_unit)
                            zetas += 1
                        elif skill['tier'] == skill['tiers'] - 1:
                            zetas += 1
                    else:
                        if skill['tier'] == skill['tiers']:
                            omicrons += 1
                            temp_unit = [unit['nameKey'], unit['rarity'], unit['gear']]
                            omicron_units.append(temp_unit)
                else:
                    if skill['tier'] == skill['tiers'] and skill['isZeta']:
                        zetas += 1

        return zetas, omicrons, omicron_units

    @staticmethod
    def get_gears(units):
        # Название, Количество, От какого рела, До какого рела
        rez = [["Т13", 0, 0, 9], ["Р1-4", 0, 1, 4], ["Р5", 0, 5, 5], ["Р6", 0, 6, 6], ["Р7", 0, 7, 7],
               ["Р8", 0, 8, 8],
               ["Р9", 0, 9, 9]]

        for unit in units:
            if unit['combatType'] == 'CHARACTER':
                for gear in rez:
                    rel = unit['relic']['currentTier'] - 2
                    if (rel >= gear[2]) and (rel <= gear[3]):
                        gear[1] += 1
        return rez

    @staticmethod
    def get_toons(units):
        list = ["Падме Амидала", "Старкиллер", "Рыцарь-джедай Реван", "Дарт Реван", "Дарт Малак", "Генерал Скайуокер",
                "Рыцарь-джедай Люк Скайуокер"]
        list2 = ["Ват Тамбор", "Ки-Ади-Мунди"]
        list3 = ["Лорд Вейдер", "Мастер-джедай Кеноби", "Мастер-джедай Люк Скайуокер", "Император Вечных ситхов",
                 "Верховный лидер Кайло Рен", "Рей"]
        list4 = ["Командир Асока Тано", "Мол", "Боба Фет (потомок джанго)"]

        rez = []
        rez2 = []
        rez3 = []
        rez4 = []
        for unit in units:
            if unit['combatType'] == 'CHARACTER':
                el = [unit['nameKey'], unit['gear'], unit['rarity']]
                if unit['nameKey'] in list:
                    rez.append(el)
                elif unit['nameKey'] in list2:
                    rez2.append(el)
                elif unit['nameKey'] in list3:
                    rez3.append(el)
                elif unit['nameKey'] in list4:
                    rez4.append(el)

        return rez, rez2, rez3, rez4

    @staticmethod
    def get_capitals(units):
        capitals = []

        for unit in units:
            if unit['combatType'] == 'SHIP' and unit['defId'].find("CAPITAL") > -1:
                capitals.append([unit['nameKey'], unit['rarity']])

        return capitals

    @staticmethod
    def get_unit_name(units, def_id):
        for unit in units:
            if unit['defId'] == def_id:
                return unit['nameKey']

    @staticmethod
    def get_arena_squad(player):
        units = player['arena']['char']['squad']

        squad = []
        for unit in units:
            squad.append(func.get_unit_name(player['roster'], unit['defId']))

        rez = ""
        for i in range(len(squad)):
            rez += squad[i]
            if i < len(squad) - 1:
                rez += ", "

        return rez

    @staticmethod
    def get_arena_ship(player):
        units = player['arena']['ship']['squad']

        squad = []
        for unit in units:
            squad.append(func.get_unit_name(player['roster'], unit['defId']))

        capital = ""
        start = ""
        reinforcement = ""
        for i in range(len(squad)):
            if i == 0:
                capital = squad[i]
            else:
                if (i > 0) and (i <= 3):
                    start += squad[i]
                    if i <= 3:
                        start += ", "
                else:
                    reinforcement += squad[i]
                    if i < len(squad) - 1:
                        reinforcement += ", "

        if capital == "":
            capital = "Отсутствует"

        if start == "":
            start = "Отсутствует"

        if reinforcement == "":
            reinforcement = "Отсутствует"

        return capital, start, reinforcement
