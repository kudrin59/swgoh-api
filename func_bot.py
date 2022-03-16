import numpy as np


class func_bot:
    @staticmethod
    def load_users():
        try:
            users = np.load('users.npy')
        except FileNotFoundError:
            users = []
            np.save("users", users)
        return users

    @staticmethod
    def save_users(users):
        np.save("users", users)
        return users

    @staticmethod
    def get_user_ally(author_id):
        users = func_bot.load_users()
        for user in users:
            if int(user[0]) == author_id:
                return user[1]
        return -1

    @staticmethod
    def set_user_ally(author_id, ally):
        users = func_bot.load_users()
        new_users = []
        for user in users:
            if int(user[0]) == author_id:
                user[1] = ally
                func_bot.save_users(users)
                return True
            new_users.append(user)

        user = [author_id, ally, 'phone']
        new_users.append(user)
        func_bot.save_users(new_users)
        return False

    @staticmethod
    def get_user_mode(author_id):
        users = func_bot.load_users()
        for user in users:
            if int(user[0]) == author_id:
                return user[2]
        return "phone"

    @staticmethod
    def set_user_mode(author_id, mode):
        users = func_bot.load_users()
        for user in users:
            if int(user[0]) == author_id:
                user[2] = "{}".format(mode)
                func_bot.save_users(users)
                return True
        return False
