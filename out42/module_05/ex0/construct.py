import os
import site
import sys


def in_virtual_env() -> bool:
    # Inside a venv, sys.prefix points to the venv while sys.base_prefix
    # still points to the Python installation the venv was created from.
    return sys.prefix != sys.base_prefix


def package_dir() -> str:
    paths: list[str] = site.getsitepackages()
    return paths[0] if paths else "unknown"


def report_open_laboratory() -> None:
    print("LABORATORY STATUS: You are working in the open")
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You are in the global environment!")
    print("Every reagent you install here leaks into the whole system.")
    print(f"Global reagent installation path: {package_dir()}")
    print()
    print("To seal the laboratory, run:")
    print("python3 -m venv lab_env")
    print("source lab_env/bin/activate # On Unix")
    print("lab_env\\Scripts\\activate # On Windows")
    print()
    print("Then run this program again.")


def report_sealed_laboratory() -> None:
    print("LABORATORY STATUS: The laboratory is sealed")
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
    print(f"Environment Path: {sys.prefix}")
    print()
    print("SUCCESS: You are working in an isolated environment!")
    print("Safe to install reagents without affecting")
    print("the global system.")
    print()
    print("Reagent installation path:")
    print(package_dir())
    print(f"(the global installation, left untouched: {sys.base_prefix})")


def main() -> None:
    if in_virtual_env():
        report_sealed_laboratory()
    else:
        report_open_laboratory()


if __name__ == "__main__":
    main()
