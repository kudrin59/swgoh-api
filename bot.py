from bridge import *


def commands():
    print("==== Список комманд ====")
    print("Информация об игроке: p <<ALLY>>")
    print("Сравнить игроков: ga <<ALLY>> <<ALLY>>")
    print()


def main():
    while True:
        commands()
        msg = input("Введите комманду: ")
        com = msg.split(" ")
        if com[1].isdigit():
            print()
            if com[0] == "p":
                bridge.player_info(com[1])
            if com[0] == "ga" and com[2].isdigit():
                bridge.players_vs([com[1], com[2]])
            print()


if __name__ == '__main__':
    main()
