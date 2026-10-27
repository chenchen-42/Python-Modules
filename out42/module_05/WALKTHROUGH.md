# Module 05: The Codex (environments, dependencies, packages, imports)

Every file was run against the subject's sample outputs; `flake8` is clean.
`mypy --strict` reports exactly one error, the one the subject asks for
(`ft_alembic_1.py`: `create_earth` doesn't exist on `alchemy`). Tested:
Python 3.12, a fresh venv, pip, pandas/numpy, python-dotenv and
`poetry lock`. **[choice]** marks decisions the subject leaves open.

**Do not submit** this `WALKTHROUGH.md`, any virtual environment, any `.env`,
`poetry.lock` or `__pycache__`: the subject lists the exact files and
forbids the venv and `.env`.

Layout (matches the subject's tree): `ex0/` and `ex1/` are self-contained
folders; exercises 2, 3 and 4 grow one package tree (`alchemy/`) at the
repository root, with the `ft_*.py` test scripts next to it.

---
# Exercise 0: The Sealed Laboratory

## ex0/construct.py

```python
import os
import site
import sys
```
`sys` describes the running interpreter, `site` knows where packages are
installed, `os.path` helps with paths. These are the only authorized modules
used here.

```python
def in_virtual_env() -> bool:
    return sys.prefix != sys.base_prefix
```
The core trick. `sys.base_prefix` is always the Python installation itself
(e.g. `/usr`). `sys.prefix` is the environment you are *in*. Outside a venv
they are equal; inside, `sys.prefix` is the venv folder (`/path/lab_env`).
So "different" means "inside a venv". (Very old `virtualenv` versions used
`sys.real_prefix`; modern venv/virtualenv/Poetry all use the comparison above.)

```python
def package_dir() -> str:
    paths: list[str] = site.getsitepackages()
    return paths[0] if paths else "unknown"
```
`site.getsitepackages()` lists the folders where `pip install` puts
packages for the **current** interpreter: the global one outside a venv,
`.../lab_env/lib/python3.X/site-packages` inside. That difference is exactly
what the subject wants displayed. The `if paths else` guards the (rare) case
of an empty list.

`report_open_laboratory()` prints the warning text from the sample.
`sys.executable` is the path of the Python binary running the script.
`"lab_env\\Scripts\\activate"` uses a doubled backslash because `\` starts an
escape sequence in a Python string; the output shows a single backslash.

`report_sealed_laboratory()`: `os.path.basename(sys.prefix)` extracts the last
part of the venv path (`lab_env`) as its name; `sys.prefix` is its full path;
`package_dir()` is the venv's own `site-packages`; the last line shows the
untouched global prefix for contrast (**[choice]**, an extra line).

`main()` calls one report or the other: "clearly different output in each
case". The `if __name__ == "__main__":` guard runs `main()` only when the
file is executed.

**Create and test the venv yourself** (the evaluator may ask you to):
```bash
python3 -m venv lab_env
source lab_env/bin/activate     # Windows: lab_env\Scripts\activate
python3 ex0/construct.py
deactivate
```
`python3 -m venv lab_env` makes a folder with a copy/symlink of the
interpreter and an empty `site-packages`. `activate` just puts
`lab_env/bin` first in your `PATH`, so `python3` and `pip` now mean the venv's.

## ex0/loading.py

```python
import importlib

REAGENTS: list[tuple[str, str]] = [
    ("pandas", "Data manipulation ready"),
    ("numpy", "Numerical computation ready"),
]
```
The declared reagents: (module name, message). A plain `import pandas` at the
top would **crash** with `ModuleNotFoundError` when pandas is missing, and
the subject says the program must not crash. Importing by *name at runtime*
fixes that, and also keeps mypy quiet about missing type stubs.

```python
def check_reagent(module_name: str, purpose: str) -> bool:
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        print(f"[MISSING] {module_name} - not installed")
        return False
    version: str = str(getattr(module, "__version__", "unknown"))
    print(f"[OK] {module_name} ({version}) - {purpose}")
    return True
```
`importlib.import_module("pandas")` is the function behind the `import`
statement, usable with a variable. `ModuleNotFoundError` is a subclass of
`ImportError`. Most libraries expose their version as `__version__`;
`getattr(obj, name, default)` reads it safely and falls back to `"unknown"`.

`main()` loops over the reagents, collects the missing names, always prints the
"pip vs Poetry" explanation, then either lists install commands for **both**
tools or prints "All reagents present and accounted for.". It never exits
with an error.

## requirements.txt and pyproject.toml

```
pandas>=2.0,<3
numpy>=1.24,<3
```
`requirements.txt` (pip) is a plain list of constraints (`>=` minimum, `<`
upper cap). Run `pip install -r ex0/requirements.txt`.

```toml
[tool.poetry]
name = "the-codex-laboratory"
version = "0.1.0"
description = "Reagents for the sealed laboratory"
authors = ["Apprentice <apprentice@example.com>"]
package-mode = false

[tool.poetry.dependencies]
python = ">=3.10,<4.0"
pandas = ">=2.0,<3"
numpy = ">=1.24,<3"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```
Same constraints in Poetry's file. `package-mode = false` tells Poetry this is
only a set of dependencies, not an installable package, so `poetry install`
doesn't look for source code to build (needs Poetry 1.8+). `python =` declares
the supported Python. I verified it with `poetry lock`, which resolved fine
(Poetry 2.x only prints deprecation warnings about `[tool.poetry]` fields;
the classic form works on both 1.x and 2.x).

**pip vs Poetry:** pip installs what you list and doesn't remember what it
resolved; Poetry resolves all dependencies together and writes the exact
versions into `poetry.lock`, so every machine gets identical installs. Poetry
also separates direct from transitive dependencies and manages the venv.

**What does a venv isolate, and what not?** It isolates *installed Python
packages* (its own `site-packages`) and which `python`/`pip` you get. It does
not isolate the OS, system libraries, environment variables, files, network,
or the Python version's own standard library (it reuses the base interpreter).

---
# Exercise 1: The Oracle

## ex1/oracle.py (line by line)

```python
KEYS = ("MATRIX_MODE", "DATABASE_URL", "API_KEY", "LOG_LEVEL", "ZION_ENDPOINT")
REQUIRED_IN_PRODUCTION = ("DATABASE_URL", "API_KEY", "ZION_ENDPOINT")
DEFAULTED = ("MATRIX_MODE", "LOG_LEVEL")
HERE = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(HERE, ".env")
GITIGNORE_PATH = os.path.join(HERE, ".gitignore")
```
The five variables of the subject; those that must exist in production;
those that have defaults. `__file__` is this script's path, so `.env` and
`.gitignore` are found **next to the script** whatever directory you run it
from (the subject runs `python3 ex1/oracle.py` from the repo root).

```python
def load_env_file() -> tuple[bool, list[str]]:
    try:
        from dotenv import dotenv_values, load_dotenv
    except ImportError:
        return (False, [])
```
The import is inside the function so a missing `python-dotenv` doesn't crash
the program: we report it later as a warning and keep reading real
environment variables.

```python
    file_values = dotenv_values(ENV_PATH)
    overridden: list[str] = []
    for key in KEYS:
        in_file: str | None = file_values.get(key)
        if key in os.environ and in_file is not None \
                and in_file != os.environ[key]:
            overridden.append(key)
    load_dotenv(ENV_PATH, override=False)
    return (True, overridden)
```
`dotenv_values` **reads** the file into a dict without touching the
environment (an empty dict if the file doesn't exist). *Before* loading, any
key already in `os.environ` came from the real environment (shell, CI,
Docker). If the file has a different value, the real environment wins, so we
record it. `load_dotenv(..., override=False)` then copies the file's values
into `os.environ` **only for keys that aren't already set**. That one
argument is the whole "environment overrides `.env`" behaviour the subject
tests with `MATRIX_MODE=production API_KEY=secret123 python3 ex1/oracle.py`.

```python
def read_setting(name: str) -> str | None:
    value: str = os.environ.get(name, "").strip()
    return value if value else None
```
`os.environ` is a dict-like of environment variables. `.get(name, "")` avoids
`KeyError`; empty or whitespace-only counts as "not set" (`None`).

```python
def has_hardcoded_secrets() -> bool:
    ...
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as file:
        source: str = file.read()
    ...
    return any(secret in source for secret in secrets)
```
A **real** check using file operations: collect the actual secret values
(`API_KEY`, `DATABASE_URL`, ignoring values shorter than 6 characters to avoid
false positives) and test whether any of them appears literally inside this
program's own source. If a secret were pasted in the code, it reports it.
(I tested that: adding the key as a comment flips the check to `[FAIL]`.)

```python
def env_file_is_gitignored() -> bool:
    ... lines = [line.strip() for line in file]
    return ".env" in lines
```
Reads `ex1/.gitignore` and checks that a line is exactly `.env`. (This
doesn't match `.env.example`, which **should** be committed as a template.)

`main()` step by step: load the file; determine the mode (default
`development`; an unknown value becomes a warning + `development`); read
the settings; build the **warnings** list for every unset key (marking those
with a default) plus python-dotenv/`.env` problems; print the status block.
**Development vs production difference** (visible in the output):
production defaults the log level to `WARNING` (development: `DEBUG`) and the
database line says "production database" instead of "local instance".
**[choice]** In production, if `DATABASE_URL`, `API_KEY` or `ZION_ENDPOINT`
is missing it prints an `ERROR` and calls `sys.exit(1)`: a clean, explained
stop with a non-zero code, not a traceback. Secrets are never printed, only
"Authenticated" / "Not authenticated". "Connected" and "Online" are
simulated messages: nothing is really contacted.

## .env.example, .gitignore, requirements.txt

`.env.example` is the committed template with **fake** placeholder values:
`cp ex1/.env.example ex1/.env`, then edit. `.gitignore` contains `.env` so the
real secrets never reach git. `requirements.txt` has `python-dotenv>=1.0`.

**Why must `.env` be git-ignored?** Git history is permanent and widely
copied: a pushed secret must be considered leaked even if you delete it
later. **Why is an environment variable better than a constant in the
code?** Code is committed, shared, reviewed and bundled; configuration can
differ per environment (dev/prod) without changing code, and secrets stay out
of the repository. **What is still not safe?** Environment variables are
readable by the process and its children, visible in some debug pages,
crash dumps, `/proc/<pid>/environ`, logs, shell history and CI output; for
real production use a secrets manager.

---
# Exercise 2: The Alembic

Vocabulary: a **module** is one `.py` file; a **package** is a folder with an
`__init__.py` that Python imports as a unit; `import x` binds a module name
`x`; `from x import y` binds just `y`.

```python
# elements.py (repository root)
def create_fire() -> str: return "Fire element created"
def create_water() -> str: return "Water element created"
# alchemy/elements.py
def create_earth() -> str: ...
def create_air() -> str: ...
```
Simple functions returning strings, as required. Two different modules both
named `elements`: the root one is imported as `elements`, the other as
`alchemy.elements`. They don't clash because the package name is part of the
path.

```python
# alchemy/__init__.py
from .elements import create_air

__all__ = ["create_air"]
```
`__init__.py` runs when you `import alchemy`. The dot in `.elements` means
"the sibling module in *this* package". It imports `create_air` into the
package's namespace, so `alchemy.create_air` exists. `create_earth` is never
imported there, so `alchemy.create_earth` does not exist.
`__all__` declares the package's public names, and satisfies the tools:
without it, flake8 reports **F401 unused import** and mypy `--strict`
refuses to treat the import as a re-export. (The subject's hint about
`__init__.py` conventions.)

**ft_alembic_0.py**: `import elements` then `elements.create_fire()`: the
plain `import ...` form; call through the module name.

**ft_alembic_1.py**: `import alchemy`, `alchemy.create_air()` works, then
`alchemy.create_earth()` raises `AttributeError`. The mypy error is expected
and kept on purpose. **[choice]** I catch the exception and print it
(the subject allows catching or not); delete the `try/except` to get the raw
traceback of the sample. The `end=""` makes the next output continue on the
same line as "Testing the hidden create_earth: ".

**"So what exactly did `__init__.py` change?"** Nothing was hidden or made
private. `__init__.py` only decides **which names are bound in the package's
namespace**. `create_earth` still exists in `alchemy/elements.py` and you can
reach it with `alchemy.elements.create_earth()` (importing the package also
loads the submodule `elements`, so `alchemy.elements` exists). Python has
no real privacy; `__init__.py` shapes the *public interface*.

---
# Exercise 3: Distillation and Transmutation

## alchemy/potions.py

```python
from elements import create_fire, create_water

from .elements import create_air, create_earth
```
Two of the four elements live **outside** the package (root `elements.py`) and
two inside. This is an **absolute** import: `from elements import ...` starts
from the top-level modules, which are searched through `sys.path`. When you
run `python3 script.py`, Python puts the script's folder (the repo root) at
`sys.path[0]`, so the root `elements.py` is found; **we never modify
`sys.path`**, as the subject forbids. The second line is a **relative**
import: `.elements` = `alchemy/elements.py`, the sibling module. (Python 3 has
no implicit relative imports, so `from elements import` inside the package
means the *root* module, not the sibling.)

`healing_potion()` / `strength_potion()` build the required strings from the
four function results with f-strings.

**ft_distillation_0.py** uses `from alchemy.potions import healing_potion,
strength_potion`: the `from ... import ...` form binds the two functions
directly, so you call them without a prefix.

## alchemy/transmutation/recipes.py

```python
from elements import create_fire            # absolute, top-level module
from alchemy.potions import strength_potion # absolute, through the package
from ..elements import create_air           # relative, one level up
```
`..` means "the parent package": from `alchemy.transmutation.recipes`,
`..elements` is `alchemy.elements`. One dot = same package, two dots = parent.
The subject requires at least one absolute and one relative import; this file
has both kinds. `alchemy/transmutation/__init__.py` (just a docstring) makes
the folder a sub-package.

**ft_transmutation_0.py**: `import alchemy.transmutation.recipes` and call
`alchemy.transmutation.recipes.lead_to_gold()`. Importing a dotted path
imports every package on the way (`alchemy`, then `alchemy.transmutation`,
then `recipes`) and binds the top name `alchemy`.

**Absolute vs relative?** Absolute imports (`alchemy.potions`) are explicit
and survive moving the file; they're preferred by PEP 8 and usually clearer.
Relative imports (`.`, `..`) keep sibling modules inside a package linked
without repeating the package name, so renaming/moving the whole package
doesn't break them. Relative imports only work **inside packages** (not in a
script run directly).

---
# Exercise 4: Avoid the Explosion

Python executes a module top to bottom when first imported, registering it in
`sys.modules` *before* it finishes. A **circular import** means A imports B
while B imports A: when B asks A for a name, A is only half-built, so the
name isn't there yet, and Python raises `ImportError ... (most likely due to a
circular import)`.

## The dark pair (fails on purpose)

```python
# dark_spellbook.py                      # dark_validator.py
from .dark_validator import \            from .dark_spellbook import \
    dark_validate_ingredients                dark_spell_allowed_ingredients
```
Both import the other **at the top**. `ft_kaboom_1.py` imports
`dark_spellbook` first: it starts, line 1 imports `dark_validator`; that
starts, line 1 asks `dark_spellbook` for `dark_spell_allowed_ingredients`,
but `dark_spellbook` is paused at its first line and has defined nothing →
`ImportError`. (If you import `dark_validator` first it also fails, in the
mirror order; I tested both.) The function bodies, written separately from
the light pair, use the ingredients `bats, frogs, arsenic, eyeball`.

**ft_kaboom_1.py** prints its three lines, then imports. The `import` comes
after the `print`s on purpose, so flake8 would say **E402**; the
`# noqa: E402` comment silences exactly that rule for that line.
`alchemy/grimoire/__init__.py` exposes only the **light** names; if it
imported the dark files, merely importing the package would explode and
`ft_kaboom_0.py` couldn't work.

## The light pair (survives)

```python
# light_spellbook.py: from .light_validator import validate_ingredients  (top)
# light_validator.py:
def validate_ingredients(ingredients: str) -> str:
    from .light_spellbook import light_spell_allowed_ingredients   # lazy
```
The spellbook imports the validator at the top; the validator imports the
spellbook **inside the function**, which runs only when called, after both
modules are fully loaded. At import time there's only a one-way dependency,
so no cycle. `validate_ingredients` lowercases the text and checks whether
any allowed ingredient appears in it (case-insensitive substring; so
"fireplace" would count as containing "fire"), returning
`"<ingredients> - VALID"` or `"- INVALID"`. `light_spell_record` uses the
verdict: `endswith(" - VALID")` (not `"VALID" in ...`, because "INVALID"
contains "VALID"!) to build "Spell recorded: ..." or "Spell rejected: ...".

**Other ways to break the cycle (be ready to discuss):** (1) move the shared
data (the allowed list) into a third module both import; (2) pass the
dependency as an argument (dependency injection); (3) import the *module*
(`from . import light_validator`) and use `light_validator.x` only at call
time; (4) merge the two files; (5) the lazy import used here. Best is
usually to **remove the cycle in the design** (option 1 or 2), and use the
lazy import as a pragmatic fix.

**"Why does only one of them explode?"** Both pairs *depend* on each other,
but only the dark pair needs the other module to be **finished loading at
import time**. The light pair postpones the need until a function is called,
when everything is loaded. The difference is one design decision (when the
dependency is resolved), not a syntax detail.

**ft_kaboom_0.py**: `from alchemy.grimoire import light_spell_record`, then
records "Fantasy" with "Earth, wind and fire" → `Spell recorded: Fantasy
(Earth, wind and fire - VALID)`.

---
# Questions to prepare

1. What does a venv isolate and not isolate? Why Poetry over requirements.txt?
2. `sys.prefix` vs `sys.base_prefix`: what does each point to?
3. Why does `override=False` matter? Why is `.env` in `.gitignore`?
4. What does `__init__.py` do? What is `__all__` for? Why F401?
5. Absolute vs relative imports; what does `..` mean?
6. Why can `potions.py` do `from elements import ...` without touching
   `sys.path`? (Script folder is `sys.path[0]`.)
7. What is a circular import at the interpreter level (`sys.modules`,
   partially initialized module)? Name three ways to fix it.
8. Live-coding candidates: add a new element to `alchemy/__init__.py`;
   expose `create_earth`; break and repair the light grimoire cycle.
