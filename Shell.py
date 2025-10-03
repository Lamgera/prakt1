import os

#конфигурация
VFS_PATH = "/vfs/path" #заглушка
STARTUP_SCRIPT = "startup_script.txt"

def execute_script(script_path):
    if not os.path.exists(script_path):
        print(f"Error: script file '{script_path}' does not exist.")
        return
    try:
        with open(script_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                print(f"VFS> {line}")
                parts = line.split()
                if not parts:
                    continue
                command = parts[0]
                args = parts[1:]

                if command == "ls":
                    print(f"ls {' '.join(args)}")
                elif command == "cd":
                    print(f"cd {' '.join(args)}")
                elif command == "exit":
                    return
                else:
                    print(f"Error: unknown command '{command}'")
    except Exception as e:
        print(f"Error executing script: {e}")

def main():
    print(f"VFS Path: {VFS_PATH}")
    print(f"Startup Script: {STARTUP_SCRIPT}")
    print()

    if STARTUP_SCRIPT:
        execute_script(STARTUP_SCRIPT)

    while True:
        try:
            user_input = input("VFS> ").strip()
            if not user_input:
                continue
            parts = user_input.split()
            command = parts[0]
            args = parts[1:]

            if command == "ls":
                print(f"ls {' '.join(args)}")
            elif command == "cd":
                print(f"cd {' '.join(args)}")
            elif command == "exit":
                break
            else:
                print(f"Error: unknown command '{command}'")
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except EOFError:
            break

if __name__ == "__main__":
    main()