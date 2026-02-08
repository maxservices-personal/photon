import sys
from .commands import (
    new,
    run,
    createapp,
    routes,
    shell,
)

COMMANDS = {
    "createproject": new.run,
    "runserver": run.run,
    "createapp": createapp.run,
    "routes": routes.run,
}

def main(argv):
    if len(argv) < 2:
        print("Usage: photon <command>")
        print("Available commands:")
        for cmd in COMMANDS:
            print(f"  {cmd}")
        sys.exit(1)

    cmd = argv[1]
    args = argv[2:]

    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

    COMMANDS[cmd](args)
