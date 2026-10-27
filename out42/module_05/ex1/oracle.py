import os
import sys

KEYS: tuple[str, ...] = ("MATRIX_MODE", "DATABASE_URL", "API_KEY",
                         "LOG_LEVEL", "ZION_ENDPOINT")
REQUIRED_IN_PRODUCTION: tuple[str, ...] = ("DATABASE_URL", "API_KEY",
                                           "ZION_ENDPOINT")
DEFAULTED: tuple[str, ...] = ("MATRIX_MODE", "LOG_LEVEL")
HERE: str = os.path.dirname(os.path.abspath(__file__))
ENV_PATH: str = os.path.join(HERE, ".env")
GITIGNORE_PATH: str = os.path.join(HERE, ".gitignore")


def load_env_file() -> tuple[bool, list[str]]:
    """Load ex1/.env without overriding the real environment.

    Returns (python-dotenv available, keys where the environment won).
    """
    try:
        from dotenv import dotenv_values, load_dotenv
    except ImportError:
        return (False, [])

    file_values = dotenv_values(ENV_PATH)
    overridden: list[str] = []
    for key in KEYS:
        in_file: str | None = file_values.get(key)
        if key in os.environ and in_file is not None \
                and in_file != os.environ[key]:
            overridden.append(key)
    load_dotenv(ENV_PATH, override=False)
    return (True, overridden)


def read_setting(name: str) -> str | None:
    value: str = os.environ.get(name, "").strip()
    return value if value else None


def has_hardcoded_secrets() -> bool:
    secrets: list[str] = []
    for name in ("API_KEY", "DATABASE_URL"):
        value: str | None = read_setting(name)
        if value is not None and len(value) >= 6:
            secrets.append(value)
    try:
        with open(os.path.abspath(__file__), "r", encoding="utf-8") as file:
            source: str = file.read()
    except OSError:
        return True
    return any(secret in source for secret in secrets)


def env_file_is_gitignored() -> bool:
    try:
        with open(GITIGNORE_PATH, "r", encoding="utf-8") as file:
            lines: list[str] = [line.strip() for line in file]
    except OSError:
        return False
    return ".env" in lines


def main() -> None:
    print("ORACLE STATUS: Consulting the configuration...")
    print()

    dotenv_ready, overridden = load_env_file()

    mode: str = read_setting("MATRIX_MODE") or "development"
    warnings: list[str] = []
    if mode not in ("development", "production"):
        warnings.append(f"MATRIX_MODE '{mode}' is unknown, "
                        "using 'development'")
        mode = "development"
    production: bool = mode == "production"

    database: str | None = read_setting("DATABASE_URL")
    api_key: str | None = read_setting("API_KEY")
    zion: str | None = read_setting("ZION_ENDPOINT")
    log_level: str = read_setting("LOG_LEVEL") or (
        "WARNING" if production else "DEBUG")

    for key in KEYS:
        if read_setting(key) is None:
            suffix: str = " (default used)" if key in DEFAULTED else ""
            warnings.append(f"{key} is not set{suffix}")
    if not dotenv_ready:
        warnings.append("python-dotenv is not installed "
                        "(only real environment variables are read)")
    elif not os.path.exists(ENV_PATH):
        warnings.append("no .env file found (copy .env.example to .env)")

    if database is None:
        db_status = "Not configured"
    elif production:
        db_status = "Connected to production database"
    else:
        db_status = "Connected to local instance"

    print("Configuration loaded:")
    print(f"Mode: {mode}")
    print(f"Database: {db_status}")
    print(f"API Access: "
          f"{'Authenticated' if api_key else 'Not authenticated'}")
    print(f"Log Level: {log_level}")
    print(f"Remote Network: {'Online' if zion else 'Offline'}")

    if warnings:
        print()
        print("Warnings:")
        for warning in warnings:
            print(f"[WARN] {warning}")

    missing: list[str] = [key for key in REQUIRED_IN_PRODUCTION
                          if read_setting(key) is None]
    if production and missing:
        print()
        print(f"ERROR: production refuses to run without: "
              f"{', '.join(missing)}")
        sys.exit(1)

    print()
    print("Configuration security check:")
    if has_hardcoded_secrets():
        print("[FAIL] A secret value appears inside the source code!")
    else:
        print("[OK] No hardcoded secrets detected")
    if env_file_is_gitignored():
        print("[OK] .env file properly ignored by git")
    else:
        print("[FAIL] .env is not listed in ex1/.gitignore")
    print("[OK] Production overrides available")
    if overridden:
        print(f"     (the environment currently overrides .env for: "
              f"{', '.join(overridden)})")

    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
