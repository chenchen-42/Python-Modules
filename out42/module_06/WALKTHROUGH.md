# Module 06: Code Nexus (abstract architecture and design patterns)

Every file was run against the subject's sample outputs (the pipeline numbers
and item ranks match exactly); `flake8` is clean. `mypy --strict` reports
exactly one error, the one the subject asks for (`numeric.ingest("foo")` in
`data_processor.py`: a `str` where `int | float | list` is expected).
**[choice]** marks decisions the subject leaves open.
Do not submit this `WALKTHROUGH.md`.

Layout: `data_processor.py`, `data_stream.py`, `data_pipeline.py` (each file
standalone, improving the previous one), packages `ex3/` and `ex4/`, and the
root scripts `battle.py`, `capacitor.py`, `tournament.py`.

Authorized imports are only `abc` and `typing`: `ABC`/`abstractmethod` for
abstract classes and `Any`/`Protocol` for typing.

---
# Exercise 0: data_processor.py

## The abstract base class

```python
from abc import ABC, abstractmethod
from typing import Any

class DataProcessor(ABC):
```
Inheriting from `ABC` makes the class **abstract**: you can't create a
`DataProcessor()` directly, and any subclass that doesn't override *every*
`@abstractmethod` can't be instantiated either (`TypeError: Can't
instantiate abstract class ...`). It is a contract: "every processor must
have `validate` and `ingest`".

```python
    def __init__(self, name: str) -> None:
        self.name: str = name
        self._queue: list[tuple[int, str]] = []
        self._total: int = 0
```
Shared state, set once in the base class. `_queue` holds waiting data as
`(rank, text)` tuples in arrival order (a FIFO queue). `_total` counts every
item **ever** ingested, never decreases, and doubles as the next rank.
The leading `_` means "internal". `name` is used by `DataStream`'s statistics.

```python
    @abstractmethod
    def validate(self, data: Any) -> bool: ...
    @abstractmethod
    def ingest(self, data: Any) -> None: ...
```
The two abstract methods, with the signatures the subject imposes. `Any`
means "any type". The docstring is the method body (an abstract method needs
no code).

```python
    def output(self) -> tuple[int, str]:
        if not self._queue:
            raise IndexError(f"{self.name}: no data to output")
        return self._queue.pop(0)
```
The one **concrete** method, shared by all subclasses (no override needed).
`pop(0)` removes and returns the **oldest** item: first in, first out. The
returned tuple is `(rank, text)`. Asking an empty processor raises a clear
`IndexError` instead of a confusing crash.

```python
    @property
    def total_processed(self) -> int: return self._total
    @property
    def remaining(self) -> int: return len(self._queue)
```
`@property` lets you read a method like an attribute (`proc.remaining`, no
parentheses), giving read-only access to the counters used by the statistics.

```python
    def _store(self, values: list[str]) -> None:
        for value in values:
            self._queue.append((self._total, value))
            self._total += 1
```
Protected helper used by the subclasses: it appends each string with its
rank (0, 1, 2, ... in processing order) and increments the counter. The rank
is **per processor and global to its lifetime**, which is why the JSON output
in the pipeline says `item_3`, `item_4`... after three items were consumed.

## The three processors

`_is_number(value)`: `isinstance(value, (int, float))` **and not** `bool`
(in Python `True` is an `int`; I exclude it so `True` isn't treated as a
number) **[choice]**.

**NumericProcessor**
```python
def validate(self, data: Any) -> bool:
    if isinstance(data, list):
        return len(data) > 0 and all(_is_number(item) for item in data)
    return _is_number(data)
```
Accepts one number, or a **non-empty** list whose items are all numbers
(mixed int/float is fine). **[choice]** An empty list is rejected: it carries
nothing to ingest, and accepting it would let the first registered processor
"swallow" empty lists in a stream. `all(...)` is `True` only if every item
passes; `isinstance(data, list)` tells the two shapes apart.

```python
def ingest(self, data: int | float | list[int | float]) -> None:
    if not self.validate(data):
        raise ValueError("Improper numeric data")
    items = data if isinstance(data, list) else [data]
    self._store([str(item) for item in items])
```
The **overriding** method has a *narrower* signature (the subject demands the
accepted types be visible). mypy accepts it because the base method takes
`Any`. Invalid data raises `ValueError("Improper numeric data")` even if the
caller skipped `validate`, so a bad value can never silently enter the
queue. `data if isinstance(data, list) else [data]` normalizes both shapes
to a list; `str(item)` converts each number to text, kept as separate
items.

**TextProcessor**: same pattern with `str` and lists of `str`; the strings are
stored as they are.

**LogProcessor**: accepts a `dict[str, str]` or a non-empty list of them.
`_is_log` checks that it's a non-empty dict whose keys and values are all
strings. `_to_text` converts an entry: if it has `log_level` and
`log_message` (as in the sample) → `"NOTICE: Connection to server"`;
otherwise a generic `key=value, key=value` string **[choice]**. `@staticmethod`
marks helpers that don't need `self`.

## The test in main()

It follows the sample: validate `42` (True) and `"Hello"` (False); call
`ingest("foo")` **without validating** inside `try/except ValueError` and print
the message; ingest `[1, 2, 3, 4, 5]`; extract 3 values with `output()`,
unpacking the tuple `rank, value = numeric.output()`. Same for text and logs.
The `ingest("foo")` line is the deliberate mypy warning.

---
# Exercise 1: data_stream.py

The processor classes are repeated (each submitted file must be standalone)
and a `DataStream` is added.

```python
class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)
```
The stream knows only the abstract type `DataProcessor`, never `NumericProcessor` and
friends. That's the point of the exercise.

```python
    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    break
            else:
                print("DataStream error - Can't process element in "
                      f"stream: {element}")
```
For each element, ask each registered processor `validate(...)`. The first
that says yes gets it (`ingest`) and the inner loop stops (`break`). **`for ... else`**:
the `else` runs only if the loop finished **without** `break`, i.e. nobody could
handle the element, so the error message is printed. Registration order
decides priority.

```python
    def print_processors_stats(self) -> None:
        ...
        print(f"{proc.name}: total {proc.total_processed} items "
              f"processed, remaining {proc.remaining} on processor")
```
No processors → `No processor found, no data`. Otherwise one line per processor.

`main()` follows the sample: stats on an empty stream; register only the
numeric processor and send the batch (4 numbers are accepted; the string, the
log list and the text list are reported); register the others; send the same
batch again; consume 3/2/1 elements using each processor's `output()` (the
`consume` helper just calls `output` N times) and print the stats again.

**How does polymorphism help here?** `process_stream` calls `validate` and
`ingest` on *whatever* object is in the list; each class supplies its own
behaviour behind the same method names. Adding a new data type means writing
one new subclass and registering it: `DataStream` doesn't change (open for
extension, closed for modification).

---
# Exercise 2: data_pipeline.py

```python
class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...
```
A **Protocol** describes a shape ("anything with a `process_output` method of
this signature") instead of a parent class. The `...` body is just a
placeholder.

```python
class CsvExportPlugin:      # note: does NOT inherit from ExportPlugin
    def process_output(self, data): ...
class JsonExportPlugin:     # neither does this one
```
This is **duck typing / structural typing**: "if it has the right method, it is
an `ExportPlugin`". mypy checks that when you pass them to `output_pipeline`.

**CsvExportPlugin**: prints `CSV Output:` then the values joined by commas.
`_csv_field` makes it **valid CSV**: a value containing a comma, a double quote
or a newline is wrapped in double quotes and inner quotes are doubled
(`"` → `""`). **JsonExportPlugin**: builds `{"item_<rank>": "<value>", ...}`
by hand; `_json_string` escapes backslash, quote, newline, carriage return
and tab so the text is valid JSON (the backslash must be replaced first,
otherwise the escapes added afterwards would be doubled).

```python
def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
    for proc in self._processors:
        count = min(nb, proc.remaining)
        if count == 0:
            continue
        batch = [proc.output() for _ in range(count)]
        plugin.process_output(batch)
```
For each processor take up to `nb` items (`min` avoids asking for more than
exist: the log processor has only 2 when 3 are requested, as in the sample),
pull them with `output()` into a list of `(rank, text)`, and hand them to the
plugin. A processor with nothing is skipped. The list comprehension
`[proc.output() for _ in range(count)]` calls `output` `count` times.

**ABC vs Protocol: the real difference.** An ABC is *nominal*: a class must
**explicitly inherit** from it, so it can also share code (like `output`) and
the check happens at instantiation. A Protocol is *structural*: nobody
inherits; compatibility is decided by matching methods, and it's checked by
the type checker (mypy), not at runtime. A plugin system wants the Protocol
because plugin authors shouldn't have to import or inherit from your base
class; they only need to provide the right method.

---
# Exercise 3: ex3 package (abstract factory + capability)

Files: `creature.py` (Creature), `capability.py` (TransformCapability),
`entities.py` (the four concrete creatures), `factories.py` (factories),
`__init__.py` (the public interface).

```python
class Creature(ABC):
    def __init__(self, name: str, creature_type: str) -> None: ...
    @abstractmethod
    def attack(self) -> str: ...
    def describe(self) -> str:
        return f"{self.name} is a {self.creature_type} type Creature"
```
An abstract class with data (name, type), one abstract method (`attack`: every
creature attacks differently) and one concrete method (`describe`, the same
for all). Methods **return** strings; the scripts print them.

```python
class TransformCapability(ABC):
    def __init__(self) -> None:
        self.transformed: bool = False
    @abstractmethod
    def transform(self) -> str: ...
    @abstractmethod
    def revert(self) -> str: ...
```
The **capability** is a *separate* abstract class that deliberately does not
inherit from `Creature`, and holds the `transformed` state.

```python
class Flameling(Creature):
    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")
    def attack(self) -> str:
        return "Flameling uses Ember!"
```
A plain entity: `super().__init__` fills the name/type, `attack` is overridden.
`Pyrodon` is the same with type `Fire/Flying`.

```python
class Shiftling(Creature, TransformCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Shiftling", "Normal")
        TransformCapability.__init__(self)
    def attack(self) -> str:
        if self.transformed:
            return "Shiftling performs a boosted strike!"
        return "Shiftling attacks normally."
```
**Multiple inheritance**: it is a `Creature` *and* has the capability. The two
parents don't call `super().__init__()` to chain to each other, so each parent's
`__init__` is called explicitly. `transform()` sets `transformed = True` and
returns the message; `revert()` sets it back; `attack()` changes with the
state, exactly as the subject says. `Morphagon` is the same with different
messages and type `Normal/Dragon`.

```python
class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature: ...
    @abstractmethod
    def create_evolved(self) -> Creature: ...

class FlameFactory(CreatureFactory):
    def create_base(self) -> Flameling: return Flameling()
    def create_evolved(self) -> Pyrodon: return Pyrodon()
```
The **abstract factory**: callers ask a factory for "the base" or "the evolved"
creature of a family and never name the concrete class. Each concrete
factory returns its own family (`FlameFactory`: Flameling → Pyrodon;
`TransformCreatureFactory`: Shiftling → Morphagon). A subclass may return a
*more specific* type than the parent promised (covariant return type), which
is why mypy still knows that `TransformCreatureFactory().create_base()` has
`transform()` while a plain `CreatureFactory` only promises a `Creature`.

```python
# ex3/__init__.py
from .factories import CreatureFactory, FlameFactory, TransformCreatureFactory
__all__ = ["CreatureFactory", "FlameFactory", "TransformCreatureFactory"]
```
The package exposes **only the three factories**; `Flameling`, `Shiftling`,
etc. aren't importable as `ex3.Flameling` (the submodule files themselves can
still be reached by path: Python doesn't enforce privacy, as in module 05).

**battle.py**: `test_factory(factory)` takes *any* `CreatureFactory`, creates
base then evolved, and calls `describe()` and `attack()`; it never mentions a
concrete class (the loop over `(factory.create_base(), factory.create_evolved())`
needs no type names thanks to inference). `test_battle(first, second)`
makes the two base entities fight.

**capacitor.py**: it needs `transform()`/`revert()`, which a plain `Creature`
doesn't have, and `ex3` doesn't expose the capability. I solved it with a
local `Protocol` called `Transformer` listing the four methods used:
structural typing again, so the script type-checks without importing anything
hidden. `demonstrate` runs describe → attack → transform → attack → revert on
the base and the evolved creature.

**Why not put `transform`/`revert` on `Creature`?** Every creature (Flameling,
Pyrodon...) would be forced to have them, even those that can't transform:
you'd need dummy methods, or errors, or flags like `can_transform`. Code
calling `creature.transform()` couldn't trust it. A separate capability
means *only* creatures that really have it can be asked, and `isinstance`
can ask the question (see exercise 4).

---
# Exercise 4: ex4 package (strategy pattern) and tournament.py

Files: `errors.py`, `strategy.py`, `strategies.py`, `__init__.py`.

```python
class StrategyError(Exception): ...
```
The dedicated exception for "this strategy can't be used on that creature".

```python
class BattleStrategy(ABC):
    label: str = "abstract"
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool: ...
    @abstractmethod
    def act(self, creature: Creature) -> None: ...
    def _invalid(self, creature: Creature) -> StrategyError:
        return StrategyError(f"Invalid Creature '{creature.name}' for this "
                             f"{self.label.lower()} strategy")
```
The abstract strategy: `is_valid` answers "can this creature use me?",
`act` does the behaviour. `label` names the strategy for the messages; the
protected helper builds the error text once for all strategies, e.g. `Invalid
Creature 'Flameling' for this aggressive strategy`.

```python
class NormalStrategy(BattleStrategy):
    def is_valid(self, creature): return True
    def act(self, creature):
        if not self.is_valid(creature): raise self._invalid(creature)
        print(creature.attack())

class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature):
        return isinstance(creature, TransformCapability)
    def act(self, creature):
        if not isinstance(creature, TransformCapability):
            raise self._invalid(creature)
        print(creature.transform()); print(creature.attack())
        print(creature.revert())
```
`NormalStrategy` suits everybody. `AggressiveStrategy` asks the **capability**
with `isinstance`, never the concrete class (`Shiftling`, `Morphagon`, or a
future creature all work). Inside `act` the `isinstance` check also lets mypy
know the creature has `transform()`/`revert()`. If the creature doesn't fit,
a `StrategyError` is raised.
**[choice]** `ex4` imports `Creature` and `TransformCapability` from the
submodules (`ex3.creature`, `ex3.capability`) because I kept `ex3/__init__.py`
limited to the factories, as the subject says. If your evaluator is fine with
it, you could also expose those two **abstract** classes in `ex3/__init__.py`
and import them as `from ex3 import ...`.

## tournament.py

```python
def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    fighters = [(factory.create_base(), strategy)
                for factory, strategy in opponents]
```
One function handles any list of `(factory, strategy)` pairs. First, create
one base entity per opponent (list comprehension building tuples).

```python
    try:
        for i, (first, first_strategy) in enumerate(fighters):
            for second, second_strategy in fighters[i + 1:]:
                ...
                first_strategy.act(first)
                second_strategy.act(second)
    except StrategyError as error:
        print(f"Battle error, aborting tournament: {error}")
```
`enumerate` gives the index `i`; `fighters[i + 1:]` (a slice) are the
opponents after `i`, so **every pair meets exactly once** (A-B, A-C, B-C) and never
itself. Each entity acts using **its own** strategy. A bad pairing raises
`StrategyError` in `act`; the `except` around **both** loops prints the
message and ends the whole tournament (the sample shows the first fighter
acting before the error, so validation happens at `act` time).

`run_tournament` prints the title and the opponents list like
`(Flameling+Normal)`, then calls `battle`. `main` runs the two tournaments
of the sample and a third one with three opponents (three battles) that I
added to show the pairing logic.

**Where did the decision move?** The tournament never checks a creature's
family or capabilities. The decision moved into the **strategy objects**
(`is_valid` + `act`) which check `isinstance(creature, TransformCapability)`.
The day you add a new capability (say `FlyCapability`) you write a new
strategy class and, if needed, a new creature; `tournament.py` and the
existing strategies stay untouched.

---
# Questions to prepare

1. What does `ABC` + `@abstractmethod` guarantee, and when does the error
   happen? (At instantiation.)
2. Why can `ingest` have a narrower signature than the base class method?
   (The base uses `Any`; in general, narrowing parameters breaks Liskov.)
3. Explain `for ... else` in `process_stream`.
4. ABC vs Protocol: nominal vs structural; why a plugin system wants a Protocol.
5. What does the rank in `output()` mean? Why a queue (`pop(0)`)?
6. Abstract factory: what does the calling code gain? Why covariant returns?
7. Why is the capability not a `Creature`? Why explicit parent `__init__` calls?
8. What does `isinstance(creature, TransformCapability)` buy you over
   checking the class name?
9. Live-coding candidates: add a new processor type (e.g. `BooleanProcessor`),
   a new export plugin (e.g. `TsvExportPlugin`), a new creature family with its
   factory, or a new `DefensiveStrategy`.
