import os
import getpass
import socket

def expand_env_variables(command):
    parts = command.split()
    expanded_parts = []
    for part in parts:
        if part.startswith('$'):
            var = part[1:]
            expanded = os.environ.get(var, '')
            expanded_parts.append(expanded)
        else:
            expanded_parts.append(part)
    return ' '.join(expanded_parts)

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
        # Раскрытие переменных окружения
        command_line = expand_env_variables(user_input)
        parts = command_line.strip().split()
        if not parts:
            continue

        cmd = parts[0]
        args = parts[1:]

        if cmd == 'exit':
            print("Exit.")
            break
        elif cmd == 'ls':
            print(f"Command: ls, Arguments: {args}")
        elif cmd == 'cd':
            print(f"Command: cd, Arguments: {args}")
        else:
            print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
