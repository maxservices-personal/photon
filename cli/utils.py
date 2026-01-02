from pathlib import Path

AUTO_START = "# ==== AUTO APPS START ===="
AUTO_END = "# ==== AUTO APPS END ===="

def register_app(app_name: str):
    router_path = Path("router.py")

    if not router_path.exists():
        raise FileNotFoundError("router.py not found in project root")

    content = router_path.read_text()

    if AUTO_START not in content or AUTO_END not in content:
        raise RuntimeError(
            "router.py is missing AUTO APPS markers"
        )

    import_line = (
        f"from apps.{app_name}.router import router as {app_name}_router\n"
        f"router.include({app_name}_router)\n"
    )

    start = content.index(AUTO_START) + len(AUTO_START)
    end = content.index(AUTO_END)

    existing_block = content[start:end]

    if import_line in existing_block:
        print(f"App '{app_name}' already registered")
        return

    new_block = f"\n{import_line}"

    updated = (
        content[:start]
        + existing_block
        + new_block
        + content[end:]
    )

    router_path.write_text(updated)
