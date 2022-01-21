from bridge import *


def commands():
    print("==== Список комманд ====")
    print("Информация об игроке: p <<ALLY>>")
    print("Сравнить игроков: ga <<ALLY>> <<ALLY>>")
    print()


def main():
    commands()
    msg = input("Введите комманду: ")
    com = msg.split(" ")

    if len(com[0]) < 1:
        return False

    if com[0] == "p":
        if len(com) < 2 or not com[1].isdigit():
            return False
        bridge.player_info(com[1])

    if com[0] == "ga":
        if len(com) < 3 or not com[1].isdigit() or not com[2].isdigit():
            return False
        bridge.players_vs([com[1], com[2]])


if __name__ == '__main__':
    main()
