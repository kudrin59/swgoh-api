class func:
    @staticmethod
    def get_gears(units):
        # Название, Количество, Необходимый тир, Необходимый релик
        rez = [["G11", 0, 11], ["G12", 0, 12], ["G13", 0, 13]]
        for unit in units:
            for gear in rez:
                if unit['gear'] == gear[2]:
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
                else:
                    if unit['nameKey'] in list2:
                        rez2.append(el)
                    else:
                        if unit['nameKey'] in list3:
                            rez3.append(el)
                        else:
                            if unit['nameKey'] in list4:
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
    def get_count_zeta(units):
        zetas = 0
        for unit in units:
            if unit['combatType'] == 'CHARACTER':
                for skill in unit['skills']:
                    if skill['isZeta'] and skill['tier'] == skill['tiers']:
                        zetas += 1
        return zetas

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
