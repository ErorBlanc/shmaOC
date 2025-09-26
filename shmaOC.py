import argparse #для чтения параметров
import os #для работы с операционной системой
import getpass #для получения имени пользователя
import socket #для работы с сетевыми функциями
import shlex #для разбора строк с поддержкой кавычек

print ("="*50)
# инициализация переменной HOME для Windows
if os.name == 'nt' and not os.environ.get('HOME'): # environ - доступ к переменным окружения операционной системы
    os.environ['HOME'] = os.environ['USERPROFILE'] #установка home = userpofile

def expand_vars(args):
    expanded = []
    for arg in args:
        modified_arg = arg.replace("$", "%") #замена $ на % для windoWS
        arg = os.path.expandvars(arg)   # раскрыть переменные %VAR% окружения
        arg = os.path.expanduser(arg)   # преобразует ~ в путь типа C:\Users\user
        expanded.append(arg)
    return expanded

def parcer(command):
    parts = shlex.split(command) # разбиваем команду на аргументы с поддержкой кавычек
    expanded = [os.path.expandvars(part) for part in parts] # раскрываем переменные окружения вида $VAR и ${VAR} в каждом аргументе
    return expanded

def commands(cmd, args, show_prompt=True):
    if show_prompt:
        print(f"> {cmd} {' '.join(args)}")  # показ введенной команды в формате ">" команда аргументы
        #обработка команд
    if cmd == 'exit':
        print("Exit.")
        exit()
    elif cmd == 'ls':
        print(f"Command: ls, Arguments: {args}")
    elif cmd == 'cd':
        print(f"Command: cd, Arguments: {args}")
    elif cmd == 'echo':
        print(" ".join(args))
    else:
        print(f"Unknown command: {cmd}")

def main():
    username = getpass.getuser() #получение имени пользователя
    hostname = socket.gethostname() #получение имени хоста - компьютера
    cwd = os.path.expanduser('~')
    # парсим аргументы командной строки
    parser = argparse.ArgumentParser() #парсер аргументов
    parser.add_argument('--vfs-path', help='Путь к VFS', default='~') #добавление аргумента для пути к VFS с значением по умолчанию ~
    parser.add_argument('--script-path', help='Путь к стартовому скрипту', default='start.sh') ## Добавление аргумента для пути к скрипту с значением по умолчанию start.sh
    parsed_args = parser.parse_args() #парсинг переданных данных

    # отладочный вывод
    print("[DEBUG] Параметры запуска:")
    print(f"VFS path: {os.path.expanduser(parsed_args.vfs_path)}")
    print(f"Script path: {os.path.expanduser(parsed_args.script_path)}\n")

    if parsed_args.script_path:
        try:
            script_path = os.path.expanduser(parsed_args.script_path) #раскрытие пути скрипту
            with open(script_path, 'r', encoding='utf-8') as f: #открытие файла для чтения
                for line in f:
                    clean_line = line.split('#')[0].strip() #удаление комментариев после решетки и пробелов
                    if clean_line:
                        parts = parcer(clean_line)
                        if parts: #если есть аргументы
                            cmd = parts[0]
                            cmd_args = expand_vars(parts[1:])
                            commands(cmd, cmd_args)
        except FileNotFoundError:
            print(f"Error скрипт {parsed_args.script_path} не найден")
            return



    while True:
        prompt = f"{username}@{hostname}:{cwd}$ " #prompt v stile shell
        try:
            user_input = input(prompt)
        except:
            break
        # получаем список аргументов
        parts = parcer(user_input)
        cmd = parts[0]
        args = parts[1:]
        # раскрываем переменные в аргументах
        args = expand_vars(args)
        commands(cmd, args)





if __name__ == "__main__":
    main()
