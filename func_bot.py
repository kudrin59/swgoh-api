import numpy as np


class func_bot:
    @staticmethod
    def load_users():
        print("Загрузка пользователей...")
        users = []
        try:
            users = np.load('users.npy')
            print(f"Пользователей загружено: {len(users)}!")
        except FileNotFoundError:
            np.save("users", users)
            print("Создан файл с пользователями!")

        return users

    @staticmethod
    def save_users(users):
        np.save("users", users)

        print("Сохранение пользователей!")

        return users

    @staticmethod
    def get_user_ally(author_id, users):
        for user in users:
            if int(user[0]) == author_id:
                return user[1]

    @staticmethod
    def set_user_ally(users, author_id, ally):
        for user in users:
            if user[0] == str(author_id):
                user[1] = ally
                func_bot.save_users(users)
                return True
        user = [author_id, ally, 'phone']
        users.append(user)
        func_bot.save_users(users)
        return False

    @staticmethod
    def set_user_mode(users, author_id, mode):
        for user in users:
            if user[0] == str(author_id):
                user[2] = "{}".format(mode)
                func_bot.save_users(users)
                return True
        return False

    @staticmethod
    def get_user_mode(author_id, users):
        for user in users:
            if int(user[0]) == author_id:
                return user[2]
        return "phone"
