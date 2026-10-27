import importlib

REAGENTS: list[tuple[str, str]] = [
    ("pandas", "Data manipulation ready"),
    ("numpy", "Numerical computation ready"),
]


def check_reagent(module_name: str, purpose: str) -> bool:
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        print(f"[MISSING] {module_name} - not installed")
        return False
    version: str = str(getattr(module, "__version__", "unknown"))
    print(f"[OK] {module_name} ({version}) - {purpose}")
    return True


def main() -> None:
    print("REAGENT STATUS: Loading reagents...")
    print()
    print("Checking dependencies:")

    missing: list[str] = []
    for module_name, purpose in REAGENTS:
        if not check_reagent(module_name, purpose):
            missing.append(module_name)

    print()
    print("pip vs Poetry:")
    print("  requirements.txt declares what to install; pip resolves it at "
          "install time.")
    print("  pyproject.toml declares the same constraints, and Poetry pins "
          "the resolved")
    print("  versions in poetry.lock so every install is identical.")
    print()

    if missing:
        print(f"Missing reagents: {', '.join(missing)}")
        print("Install them with pip:")
        print("  pip install -r ex0/requirements.txt")
        print("Or with Poetry:")
        print("  poetry install")
        print("  poetry run python ex0/loading.py")
    else:
        print("All reagents present and accounted for.")


if __name__ == "__main__":
    main()
