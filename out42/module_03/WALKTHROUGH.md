# Module 03: Data Quest (collections)

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

## ex0: ft_command_quest.py

```python
print(f"Program name: {sys.argv[0]}")
```
`argv[0]` is the script name exactly as typed (`ft_command_quest.py`).

```python
    if len(sys.argv) == 1:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {len(sys.argv) - 1}")
        position: int = 1
        for argument in sys.argv[1:]:
            print(f"Argument {position}: {argument}")
            position += 1
    print(f"Total arguments: {len(sys.argv)}")
```
- Only the script name present means no user arguments.
- `sys.argv[1:]` is a **slice**: a new list without the first item. That is
  one way to avoid printing the program name again (the subject says to be
  ready to discuss alternatives: `range(1, len(argv))` with indexes, or
  `argv.pop(0)`, or `enumerate(argv[1:], 1)`).
- `range` and `enumerate` are not in this exercise's authorized list, so a
  manual counter `position` is used.
- "Total" counts the script name too, which is why `hello world 42` gives 4.

## ex1: ft_score_analytics.py

```python
    scores: list[int] = []
    for argument in sys.argv[1:]:
        try:
            scores.append(int(argument))
        except ValueError:
            print(f"Invalid parameter: '{argument}'")
```
Start with an empty list. `int("abc")` raises `ValueError`; we catch it,
report it, and **continue with the next argument**: invalid values are
discarded, valid ones kept.

```python
    if len(scores) == 0:
        print("No scores provided. "
              "Usage: python3 ft_score_analytics.py <score1> <score2> ...")
        return
```
Covers both "no arguments" and "only invalid arguments". The two adjacent
strings are joined by Python into one.

```python
    total: int = sum(scores)
    ...
    print(f"Average score: {total / len(scores)}")
    print(f"High score: {max(scores)}")
    print(f"Low score: {min(scores)}")
    print(f"Score range: {max(scores) - min(scores)}")
```
`/` always gives a float, so `9650 / 5` prints `1930.0` as in the sample.
No division by zero is possible: we returned earlier if the list is empty.

## ex2: ft_coordinate_system.py

```python
def get_player_pos() -> tuple[float, float, float]:
    prompt: str = "Enter new coordinates as floats in format 'x,y,z': "
    while True:
```
`while True` = retry forever; the only exits are `return` statements.

```python
        try:
            raw: str = input(prompt)
        except EOFError:
            print("\nNo more input, using (0.0, 0.0, 0.0)")
            return (0.0, 0.0, 0.0)
```
**[choice]** If input is closed, an infinite retry loop would be bad, so
we fall back to the origin. Remove it if your evaluator doesn't care.

```python
        parts: list[str] = raw.split(",")
        if len(parts) != 3:
            print("Invalid syntax")
            continue
```
`"1.0 , 2.5, 3.0".split(",")` gives `["1.0 ", " 2.5", " 3.0"]`. Not exactly
3 pieces means wrong syntax; `continue` jumps back to the top of the loop
(asks again).

```python
        values: list[float] = []
        try:
            for part in parts:
                values.append(float(part))
        except ValueError as error:
            print(f"Error on parameter '{part.strip()}': {error}")
            continue
        return (values[0], values[1], values[2])
```
`float()` tolerates surrounding spaces, so `" 2.5"` works. On failure the
exception message is `could not convert string to float: 'abc'`, the text
in the example; `part` still holds the guilty piece after the exception.
Valid: build and return a **tuple** (immutable "data written in stone").

```python
def distance(a, b):
    x1, y1, z1 = a
    x2, y2, z2 = b
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
```
**Tuple unpacking** splits a 3-tuple into three variables. The formula is
the 3D Pythagorean theorem; `**2` is "squared".

`main()` uses `round(..., 4)` as authorized, and compares with the center
`(0.0, 0.0, 0.0)`. Note: `float("nan")` and `"inf"` are accepted by
`float()`; the subject doesn't ask to reject them.

## ex3: ft_achievement_tracker.py

```python
def gen_player_achievements() -> set[str]:
    count: int = random.randint(10, 15)
    return set(random.sample(ALL_ACHIEVEMENTS, count))
```
`randint(10, 15)` = random number of achievements (both ends included).
`random.sample(list, k)` picks `k` **distinct** items, so no duplicates, and
`set(...)` turns the list into a set. The achievement list has 25 entries and
players take 10 to 15 of them, which makes "common" and "only X has"
non-empty most of the time (the subject's hint). A **set** is unordered with
unique items, which is why the printed order changes at every run. An empty
set prints `set()` because `{}` already means an empty *dict*.

```python
    players: list[tuple[str, set[str]]] = [("Alice", gen...()), ...]
```
`dict` isn't introduced yet in this exercise, so players are a list of
`(name, set)` tuples.

```python
    distinct: set[str] = set()
    common: set[str] = players[0][1]
    for _, achievements in players:
        distinct = distinct.union(achievements)
        common = common.intersection(achievements)
```
- `union` = everything anyone has; `intersection` = only what everybody has.
  `common` starts as the first player's set and is whittled down by each player.
- `for _, achievements in players` unpacks each tuple; `_` is the
  conventional name for "I don't need this".

```python
    for name, achievements in players:
        others: set[str] = set()
        for other_name, other_achievements in players:
            if other_name != name:
                others = others.union(other_achievements)
        print(f"Only {name} has: {achievements.difference(others)}")
```
For each player, build the union of **everyone else's** sets, then
`difference` keeps what is in mine and not in theirs.

```python
    everything: set[str] = set(ALL_ACHIEVEMENTS)
    ... everything.difference(achievements)
```
"Missing to have them all" is measured against the **full** achievement list
(the sample output shows 'Hidden Path Finder' as missing although nobody has
it, which confirms that).

## ex4: ft_inventory_system.py

```python
def parse_inventory(arguments: list[str]) -> dict[str, int]:
    inventory: dict[str, int] = {}
    for argument in arguments:
        parts: list[str] = argument.split(":")
        if len(parts) != 2 or parts[0] == "":
            print(f"Error - invalid parameter '{argument}'")
            continue
```
`"sword:1".split(":")` gives `["sword", "1"]`. `"hello"` gives 1 piece and
`"a:b:c"` gives 3, so both are "invalid syntax". An empty name (`":5"`) is
rejected too.

```python
        name: str = parts[0]
        if name in inventory:
            print(f"Redundant item '{name}' - discarding")
            continue
```
`in` on a dict tests the **keys**. The first occurrence wins.

```python
        try:
            quantity: int = int(parts[1])
        except ValueError as error:
            print(f"Quantity error for '{name}': {error}")
            continue
        if quantity < 0:
            ...
        inventory.update({name: quantity})
```
`int("value")` fails with the message from the sample. **[choice]** negative
quantities are rejected (not in the subject, but they would break
percentages). `dict.update({...})` adds the pair (it is the authorized
alternative to `inventory[name] = quantity`).

```python
    items: list[str] = list(inventory.keys())
    total: int = sum(inventory.values())
```
`keys()` / `values()` are "views" of the dict; `list()` makes a real list of
names; `sum` adds all quantities.

```python
        for item in items:
            percent: float = round(inventory[item] / total * 100, 1)
```
Share = quantity / total * 100, rounded to 1 decimal (5/12 gives 41.7). The
guard `total == 0` avoids a `ZeroDivisionError` with an empty inventory.

```python
        most: str = items[0]
        least: str = items[0]
        for item in items:
            if inventory[item] > inventory[most]:
                most = item
            if inventory[item] < inventory[least]:
                least = item
```
`max`/`min` aren't authorized here, so we search by hand. Starting at the
first item and using **strict** `>` / `<` means that on a tie, the first
item from the command line is kept (the subject's rule). Last step: add
`magic_item` and print again.

## ex5: ft_data_stream.py

```python
def gen_event() -> Generator[tuple[str, str], None, None]:
    while True:
        yield (random.choice(PLAYERS), random.choice(ACTIONS))
```
A **generator function** contains `yield`. Calling it doesn't run the body,
it returns a generator object. Each `next(gen)` runs the body until the next
`yield`, hands out the value, and **pauses there** keeping all its state. So
an infinite `while True` is safe: values are produced on demand, nothing is
stored (that is the memory-saving superpower). `Generator[Y, S, R]` means
yields of type Y, accepts sends of type S, returns R; `None, None` for the
last two.

```python
    stream = gen_event()
    for number in range(1000):
        name, action = next(stream)
        print(f"Event {number}: Player {name} did action {action}")
```
One generator object, asked 1000 times. `name, action = ...` unpacks the
tuple.

```python
    events: list[tuple[str, str]] = []
    for _ in range(10):
        events.append(next(stream))
```
Ten more events from the same stream, collected into a list.

```python
def consume_event(events):
    while len(events) > 0:
        index: int = random.randrange(len(events))
        yield events.pop(index)
```
Another generator: pick a random valid position, `pop(index)` **removes and
returns** that element, `yield` hands it out. Loop until the list is empty.
In `main`, `for event in consume_event(events):` calls `next()` for you until
the generator finishes. Because `pop` runs *before* the `yield`, the
`print(... events)` inside the loop shows the list already without that item,
like the sample.

## ex6: ft_data_alchemist.py

```python
all_cap = [p.capitalize() for p in players]
only_cap = [p for p in players if p == p.capitalize()]
```
A **list comprehension** `[expression for item in iterable if condition]` is
a compact `for` + `append`. `capitalize()` makes the first letter upper and
the rest lower. A name "is capitalized" if it equals its own capitalized
version (`"Alice" == "Alice"`, `"bob" != "Bob"`).

```python
scores = {p: random.randint(0, 1000) for p in all_cap}
```
A **dict comprehension** `{key: value for ...}`: one random score per name.

```python
average: float = sum(scores.values()) / len(scores)
high = {p: s for p, s in scores.items() if s > average}
```
`items()` yields `(key, value)` pairs. Filtering with `s > average` keeps
only the above-average players. I compare against the unrounded average and
print `round(average, 2)`.

---
# Things evaluators like to ask

1. List vs tuple vs set vs dict: when to use each? (ordered+mutable / ordered+immutable+hashable / unique+unordered / key to value)
2. Why can a generator be infinite? (lazy: one value at a time)
