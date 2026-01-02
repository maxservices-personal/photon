import sys
from .commands import (
    new,
    run,
    createapp,
    routes,
    shell,
)

COMMANDS = {
    "new": new.run,
    "run": run.run,
    "createapp": createapp.run,
    "routes": routes.run,
    "shell": shell.run,
}

def main():
    if len(sys.argv) < 2:
        print("Usage: photon <command>")
        print("Available commands:")
        for cmd in COMMANDS:
            print(f"  {cmd}")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

    COMMANDS[cmd](args)
