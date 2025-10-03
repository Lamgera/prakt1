import os
import json
import base64
from datetime import datetime

VFS_JSON_FILE = 'vfs.json'
STARTUP_SCRIPT = "startup_script.txt"

vfs_data = {}

def load_vfs_from_json():
    global vfs_data
    if not os.path.exists(VFS_JSON_FILE):
        print(f"VFS file '{VFS_JSON_FILE}' not found. Creating default VFS...")
        create_default_vfs()
    try:
        with open(VFS_JSON_FILE, 'r') as f:
            raw_data = json.load(f)
        vfs_data = decode_base64_data(raw_data)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{VFS_JSON_FILE}'.")
        return False
    except Exception as e:
        print(f"Error loading VFS: {e}")
        return False
    return True

def create_default_vfs():
    default_data = {
        "readme.txt": "Welcome to VFS",
        "bin": {
            "test.bin": base64.b64encode(b"binary data").decode('ascii')
        },
        "docs": {
            "doc.txt": "Documentation here"
        }
    }
    with open(VFS_JSON_FILE, 'w') as f:
        json.dump(default_data, f, indent=2)

def decode_base64_data(data):
    if isinstance(data, dict):
        result = {}
        for k, v in data.items():
            if isinstance(v, str) and k.endswith('.bin'):
                result[k] = base64.b64decode(v).decode('utf-8', errors='ignore')
            elif isinstance(v, dict):
                result[k] = decode_base64_data(v)
            else:
                result[k] = v
        return result
    return data

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
                    ls_command(args)
                elif command == "cd":
                    cd_command(args)
                elif command == "uptime":
                    uptime_command()
                elif command == "tree":
                    tree_command(args)
                elif command == "date":
                    date_command()
                elif command == "cp":
                    cp_command(args)
                elif command == "exit":
                    return
                else:
                    print(f"Error: unknown command '{command}'")
    except Exception as e:
        print(f"Error executing script: {e}")

def resolve_path(path_str, start_node=None):
    current = start_node if start_node else vfs_data
    parts = path_str.split('/')
    for part in parts:
        if part == '.' or part == '':
            continue
        if part in current and isinstance(current[part], dict):
            current = current[part]
        else:
            return None
    return current

def cp_command(args):
    if len(args) != 2:
        print("cp: missing destination or source")
        return
    src_path = args[0]
    dst_path = args[1]

    # Find source
    src_parts = src_path.split('/')
    src_name = src_parts[-1]
    src_parent_path = '/'.join(src_parts[:-1])
    src_parent = resolve_path(src_parent_path)
    if not src_parent or src_name not in src_parent:
        print(f"cp: cannot stat '{src_path}': No such file or directory")
        return

    # Find destination parent
    dst_parts = dst_path.split('/')
    dst_name = dst_parts[-1]
    dst_parent_path = '/'.join(dst_parts[:-1])
    dst_parent = resolve_path(dst_parent_path)
    if not dst_parent:
        print(f"cp: cannot stat '{dst_path}': No such file or directory")
        return

    # Copy item
    src_item = src_parent[src_name]
    dst_parent[dst_name] = src_item
    print(f"cp: '{src_path}' -> '{dst_path}'")

def ls_command(args):
    path = args[0] if args else '.'
    current = resolve_path(path)
    if current is None:
        print(f"ls: cannot access '{path}': No such file or directory")
        return
    items = list(current.keys())
    print(' '.join(items))

def cd_command(args):
    path = args[0] if args else '/'
    if path == '..':
        print("cd: cannot go up from root")
        return
    current = resolve_path(path)
    if current is None:
        print(f"cd: no such directory: {path}")
        return
    print(f"cd: {path}")

def uptime_command():
    print("0 days, 0 hours, 0 minutes")

def tree_command(args):
    path = args[0] if args else '.'
    current = resolve_path(path)
    if current is None:
        print(f"tree: cannot access '{path}': No such file or directory")
        return
    def print_tree(node, prefix=""):
        keys = list(node.keys())
        for i, key in enumerate(keys):
            is_last = i == len(keys) - 1
            print(f"{prefix}{'└── ' if is_last else '├── '}{key}")
            if isinstance(node[key], dict):
                extension = "    " if is_last else "│   "
                print_tree(node[key], prefix + extension)
    print_tree(current)

def date_command():
    now = datetime.now()
    print(now.strftime("%a %b %d %H:%M:%S %Y"))

def main():
    print(f"VFS JSON: {VFS_JSON_FILE}")
    print(f"Startup Script: {STARTUP_SCRIPT}")
    print()

    if not load_vfs_from_json():
        return

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
                ls_command(args)
            elif command == "cd":
                cd_command(args)
            elif command == "uptime":
                uptime_command()
            elif command == "tree":
                tree_command(args)
            elif command == "date":
                date_command()
            elif command == "cp":
                cp_command(args)
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