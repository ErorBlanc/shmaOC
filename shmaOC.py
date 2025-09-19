import os
import getpass
import socket
import shlex

HOME = os.path.expanduser("~")
def expand_vars(args):
    expanded = []
    for arg in args:
        arg = os.path.expandvars(arg)   # раскрыть переменные $VAR
        arg = os.path.expanduser(arg)   # раскрыть ~
        expanded.append(arg)
    return expanded

def parcer(command):
    # Разбиваем команду на аргументы с поддержкой кавычек
    parts = shlex.split(command)
    # Раскрываем переменные окружения вида $VAR и ${VAR} в каждом аргументе
    expanded = [os.path.expandvars(part) for part in parts]
    return expanded


def main():
    username = getpass.getuser()
    hostname = socket.gethostname()
    cwd = os.path.expanduser('~')

    while True:
        prompt = f"{username}@{hostname}:{cwd}$ "
        try:
            user_input = input(prompt)
        except:
            break
        # Получаем список аргументов
        parts = parcer(user_input)
        cmd = parts[0]
        args = parts[1:]

        # Раскрываем переменные в аргументах
        args = expand_vars(args)

        if cmd == 'exit':
            print("Exit.")
            break
        elif cmd == 'ls':
            print(f"Command: ls, Arguments: {args}")
        elif cmd == 'cd':
            print(f"Command: cd, Arguments: {args}")
        elif cmd == '$HOME':
            print(HOME)

        else:
            print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
