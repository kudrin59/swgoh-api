class func:
    @staticmethod
    def get_zeta_omicron(sw, units):
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
                if skill['isZeta']:
                    if skill['id'] in omicron_skills:
                        if skill['tier'] == skill['tiers']:
                            omicrons += 1
                            temp_unit = [unit['nameKey'], unit['rarity'], unit['gear']]
                            omicron_units.append(temp_unit)
                        elif skill['tier'] == skill['tiers'] - 1:
                            zetas += 1
                    else:
                        if skill['tier'] == skill['tiers']:
                            zetas += 1

        return zetas, omicrons, omicron_units

    @staticmethod
    def get_gears(units):
        # Название, Количество, От какого рела, До какого рела
        rez = [["Т13", 0, 0, 9], ["Р1-4", 0, 1, 4], ["Р5", 0, 5, 5], ["Р6", 0, 6, 6], ["Р7", 0, 7, 7], ["Р8", 0, 8, 8], ["Р9", 0, 9, 9]]
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
                capitals.append(unit['nameKey'] + ": " + str(unit['rarity']) + "⭐")

        rez = ""
        for i in range(len(capitals)):
            rez += capitals[i]
            if i < len(capitals) - 1:
                rez += ", "

        return rez

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
