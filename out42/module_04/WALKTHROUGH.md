# Module 04: Data Archivist (file operations)

Every file in this module was run against the subject's sample outputs, and
`flake8` is clean on all of them. `mypy --strict` is clean too.

**Before you read: how to use this for your defense.** Your own AI rules
say you must be able to explain everything you hand in. So: read a
program, close this file, retype it from memory, run it, then explain it
out loud to a peer. Where I made a design choice that the subject leaves
open, I flag it with **[choice]**, so you can defend or change it.

Concepts that come back all the time:

- **f-string**: `f"x is {x}"` puts the value of `x` inside the text.
- **Type hint**: `name: str` / `-> None` are labels for mypy. Python ignores them
  at runtime.
- **`if __name__ == "__main__":`**: `__name__` is `"__main__"` only when the
  file is run directly (`python3 file.py`), not when it is imported by
  another file. It lets a file be both a program and a reusable module.
- **Exception**: an error object that travels up the call stack until some
  `except` catches it; if nobody does, the program crashes.

---

## ex0: ft_ancient_text.py

```python
import sys
from typing import IO
```
`sys` gives `sys.argv`, the list of command-line words: `argv[0]` is the
script name, `argv[1:]` are your arguments. `IO` is only used for a type
hint: it describes "a file object". (Answer to the subject's question:
`open()` returns a file object, concretely `io.TextIOWrapper` in text mode;
`IO[str]` is the typing name for "a file that reads/writes `str`".)

```python
def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return
```
Exactly one argument is required, so `argv` must have 2 items (script +
file). Otherwise print usage and `return` (leave the function = end the
program).

```python
    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{filename}'")
```
Store the name, print the header and the "Accessing" line.

```python
    file: IO[str]
    try:
        file = open(filename, "r")
    except OSError as error:
        print(f"Error opening file '{filename}': {error}")
        return
```
- `file: IO[str]` only *declares* the variable's type. Without it mypy
  would complain that `file` may not exist after the `try`.
- `open(filename, "r")` opens for reading text. It can fail: missing file
  (`FileNotFoundError`, Errno 2), no permission (`PermissionError`,
  Errno 13), it is a directory (`IsADirectoryError`). All three are
  subclasses of `OSError`, so one `except OSError` covers the "various
  failure cases" the subject asks for.
- `as error` binds the exception object; printing it gives exactly
  `[Errno 2] No such file or directory: 'foo'`, the text in the example.
- Nothing was opened, so nothing to close: just `return`.

```python
    try:
        content: str = file.read()
    except (OSError, UnicodeDecodeError) as error:
        print(f"Error reading file '{filename}': {error}")
        file.close()
        return
```
`read()` loads the whole file into one string. It is a separate `try`
because reading can fail too (a binary file raises `UnicodeDecodeError`,
which is *not* an `OSError`, so it is listed explicitly). We close the file
before leaving, otherwise we would leak it.

```python
    print("---")
    print()
    print(content)
    print("---")
    file.close()
    print(f"File '{filename}' closed.")
```
`print()` alone prints an empty line. `content` already ends with `\n`, and
`print` adds another, which produces the blank line before the closing
`---`, exactly like the example. `close()` releases the file back to the OS.

```python
if __name__ == "__main__":
    main()
```
Entry point, explained above.

## ex1: ft_archive_creation.py

The subject says "use the code from the previous exercise", so ex0's logic
is split into functions.

`read_file(filename) -> str | None`: same open/read/close as ex0, but it
**returns** the content, or `None` when something failed. `str | None`
(Python 3.10 syntax) means "either a string or None". In `main`,
`if content is None: return` stops the program when reading failed.

```python
def transform(content: str) -> str:
    result: str = ""
    for line in content.splitlines():
        result += line + "#\n"
    return result
```
`splitlines()` cuts the text into a list of lines *without* the `\n`. For
each line we append `line + "#" + newline`. So every line ends with `#`
and the result ends with a newline, like the original.

```python
def save_file(filename: str, data: str) -> None:
    print(f"Saving data to '{filename}'")
    ...
        file = open(filename, "w")
```
Mode `"w"` = write: it **creates** the file or **truncates** (empties) it if
it exists. That is the subject's hint "create the file or replace it".
Failure on open (e.g. `/etc/passwd` without rights) prints the error and
`Data not saved.`. `file.write(data)` can fail too (disk full), hence the
second `try`. Success prints `Data saved in file '...'`.

```python
    try:
        new_name: str = input("Enter new file name (or empty): ")
    except EOFError:
        new_name = ""
    if new_name == "":
        print("Not saving data.")
    else:
        save_file(new_name, new_content)
```
`input()` shows the prompt and returns what the user typed. If stdin is
closed (Ctrl-D, or a pipe with no data) it raises `EOFError`; we treat that
like an empty answer so the program never crashes. Empty = don't save.

## ex2: ft_stream_management.py

The three streams: **stdin** (0, input), **stdout** (1, normal output),
**stderr** (2, errors). They are separate so you can redirect them
independently (`2> errors.txt`).

```python
print(f"[STDERR] Error opening file '{filename}': {error}", file=sys.stderr)
```
`print(..., file=sys.stderr)` sends the text to stream 2 instead of 1.
The `[STDERR]` prefix is required by the subject. The line is split over two
lines inside the parentheses to respect flake8's 79-character limit.

```python
def ask_file_name() -> str:
    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    line: str = sys.stdin.readline()
    return line.strip()
```
This replaces `input()`:
- `sys.stdout.write(text)` prints text *without* adding a newline.
- `flush()` forces it out now. Terminal output is line-buffered: text
  without a `\n` can sit in a buffer, so the prompt might appear *after*
  you typed. `flush()` prevents that.
- `sys.stdin.readline()` reads one line **including** the trailing `\n`
  (and returns `""` at end of input).
- `strip()` removes that `\n` (and spaces), so an empty answer becomes `""`.

Everything else is identical to ex1 except that errors go to stderr.

## ex3: ft_vault_security.py

```python
def secure_archive(
    filename: str,
    action: str = "read",
    content: str = "",
) -> tuple[bool, str]:
```
Mandatory `filename`; optional `action` (**[choice]**: a string, `"read"` or
`"write"`); optional `content` to write. Defaults make
`secure_archive("x")` mean "read x". It returns a tuple
`(success, text)`, where `text` is the file content, a success message,
or an error message.

```python
    try:
        if action == "read":
            with open(filename, "r") as file:
                return (True, file.read())
```
**The `with` statement** (context manager): it opens the file, runs the
indented block, and **always** closes the file at the end, even if an
exception happens or you `return` inside the block. That replaces the
manual `close()` (and the "forgot to close on the error path" bugs of
ex0-ex2). `as file` names the file object.

```python
        if action == "write":
            with open(filename, "w") as file:
                file.write(content)
            return (True, "Content successfully written to file")
        return (False, f"Unknown action '{action}' (use 'read' or 'write')")
    except (OSError, UnicodeError) as error:
        return (False, str(error))
```
One `try` wraps everything. Any I/O failure lands in `except`, and
`str(error)` gives the message required by the example. Unknown action
returns `False` with a message instead of crashing.

`main()` replays the example: nonexistent file, inaccessible file, regular
file, then writes what it read into a new file (`result[1]` is the text
part of the tuple).

**Careful when testing:** `/etc/master.passwd` exists on BSD/macOS only.
On Linux it gives Errno 2, so I used `/etc/shadow` (readable by root only,
so run your test as a normal user to see Errno 13).

---
# Things evaluators like to ask

1. Why `with` instead of `close()`? (closes on every path, even errors)
2. Why flush stdout before reading stdin? (buffering of text with no `\n`)
3. Why separate stderr from stdout? (redirect/pipe independently)
