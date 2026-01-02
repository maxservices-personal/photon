import os
from photon.templates.project import PROJECT_TEMPLATE

def run(args):
    if not args:
        print("Usage: photon new <project_name>")
        return

    name = args[0]

    if os.path.exists(name):
        print("Directory already exists")
        return

    os.makedirs(name)
    os.chdir(name)

    for path, content in PROJECT_TEMPLATE.items():
        dir_path = os.path.dirname(path)

        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        with open(path, "w") as f:
            f.write(content)

    print(f"Photon project '{name}' created")
