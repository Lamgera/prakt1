import sys

def main():
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