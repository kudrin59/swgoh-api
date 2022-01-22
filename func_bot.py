import numpy as np


class func_bot:
    @staticmethod
    def load_users():
        users = []
        try:
            users = np.load('users.npy')
        except FileNotFoundError:
            np.save("users", users)

        print("Загрузка пользователей!")
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
