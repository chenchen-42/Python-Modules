# Module 01: Code Cultivation (OOP)

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

Vocabulary: **class** = blueprint; **instance/object** = one thing made
from it; **attribute** = data stored on the object; **method** = function
of the class; **`self`** = the instance the method is called on;
**`__init__`** = constructor, runs automatically on creation.

## ex0: ft_garden_intro.py

Three variables and a few prints, inside `main()` called under the
`if __name__ == "__main__":` guard.

*Why the guard matters (defense question):* when Python imports a file it
executes it. Without the guard, importing would also run the program and
print things. With it, the code runs only when the file is executed directly.

*Shebang:* a first line `#!/usr/bin/env python3` tells the OS which
interpreter runs the file, so after `chmod +x ft_garden_intro.py` you can
run `./ft_garden_intro.py`. `env` finds `python3` wherever it is installed.
Without the line, `./file.py` would be interpreted as a shell script. The
evaluator will ask you to add it live, so try it once.

## ex1: ft_garden_data.py

```python
class Plant:
    name: str
    height: int
    days: int

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.days} days old")
```
The three lines declare the attributes' types (mypy needs them; they don't
create values). `show` reads the attributes through `self`.

```python
    rose: Plant = Plant()
    rose.name = "Rose"
    rose.height = 25
    rose.days = 30
```
`Plant()` **instantiates** the class (creates an empty object); then the
attributes are **set**, as the subject describes. Three plants = three
separate objects of the same class, each with its own values. The
weakness (what the hint asks about): it takes 4 lines per plant, and you can
forget to set an attribute, which would crash `show()`. ex3 fixes it.

## ex2: ft_plant_growth.py

New: `growth_rate` attribute and two methods:
```python
    def grow(self) -> None:
        self.height += self.growth_rate

    def age(self) -> None:
        self.days += 1
```
`+=` adds in place. Note the attribute is named `days`, **not** `age`: an
attribute `age` would collide with the method `age()`. Different plants
"evolve differently" through their own `growth_rate`.

`show` uses `round(self.height, 1)` because float arithmetic accumulates
tiny errors (`25.0 + 0.8 + 0.8 + 0.8` is `27.400000000000002`).

```python
    start_height: float = rose.height
    for day in range(1, 8):
        ...
    print(f"Growth this week: {round(rose.height - start_height, 1)}cm")
```
Save the starting height, simulate days 1 to 7 (`range(1, 8)` stops
before 8), then read the final height and subtract.

## ex3: ft_plant_factory.py

```python
    def __init__(self, name: str, height: float, days: int,
                 growth_rate: float = 0.8) -> None:
        self.name: str = name
        self.height: float = float(height)
        ...
```
`__init__` runs right at `Plant("Rose", 25.0, 30)`: creation and
initialization in one step, and you can't forget an attribute anymore.
`growth_rate=0.8` is a **default argument**, so it is optional. `float(height)`
makes sure an int like `25` is stored as `25.0`.

`show()` is unchanged; the demo prints `"Created: "` with `end=""` (no
newline) and then calls `show()`, which prints the rest of the line.

## ex4: ft_garden_security.py

**Encapsulation** = hide the data, expose controlled methods. The leading
underscore (`_height`) is the Python *convention* "protected: don't touch
from outside". (Double underscore `__height` would trigger *name mangling*;
the subject forbids that.)

```python
        self._height: float = 0.0
        self._days: int = 0
        ...
        self.set_height(height)
        self.set_age(days)
```
The constructor starts with safe defaults (0) and then goes through the
**same validating setters** as everyone else. If the given value is
negative, the setter prints the error and the default stays, "creating the
plant with default values".

```python
    def set_height(self, height: float) -> bool:
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            return False
        self._height = float(height)
        return True
```
Validate first, store only if valid. **[choice]** it returns `True`/`False`
so the caller knows whether the update was accepted (that's how `main` can
print "Height updated" or "Height update rejected" truthfully, while the
class prints the "Error..." line itself, as the subject wants). The getters
`get_height()` / `get_age()` give read access.

## ex5: ft_plant_types.py

**Inheritance**: `class Flower(Plant)` means a Flower *is a* Plant and gets
all its attributes and methods for free.

```python
class Flower(Plant):
    def __init__(self, name, height, days, color, growth_rate=0.8) -> None:
        super().__init__(name, height, days, growth_rate)
        self._color: str = color
        self._bloomed: bool = False
```
`super()` = "the parent class". `super().__init__(...)` runs `Plant`'s
constructor (which sets name/height/age and validates), so no duplicated
code; then the Flower adds its own attributes.

```python
    def show(self) -> None:
        super().show()
        print(f" Color: {self._color}")
        ...
```
**Override**: same method name replaces the parent's for Flowers, but it
first calls `super().show()` to reuse the standard line, then adds its
extras. `bloom()` flips `_bloomed`, and `show()` prints one of the two
messages depending on it.

`Tree` adds `_trunk_diameter` and `produce_shade()`, and a `show()` that
appends the trunk line. Its default `growth_rate` is slower (0.1).

`Vegetable` adds `_harvest_season` and `_nutritional_value` (starts at 0).
It overrides `grow()` and `age()`, each calling `super()` first and then
adding `0.5` to the nutritional value. **[choice]** the subject says the
value must rise with both calls and the sample shows 20 after 20 grow+age
days, so each call adds half a point. `:g` in `f"{value:g}"` prints `20.0`
as `20` and `0.5` as `0.5`.

`Plant.age` now takes `days: int = 1` so one call can age a plant several
days (used in ex6). The Vegetable override keeps a compatible signature
(mypy checks that overrides accept the same arguments).

In `main`: `for _ in range(20): tomato.grow(); tomato.age()` simulates 20
days. With `growth_rate=2.1`, `5.0 + 20*2.1 = 47.0` as in the example.

## ex6: ft_garden_analytics.py

**Static method** (`@staticmethod`): a function that lives in the class
namespace but receives neither `self` nor `cls`.
```python
    @staticmethod
    def is_older_than_one_year(days: int) -> bool:
        return days > 365
```
It's called on the class: `Plant.is_older_than_one_year(400)`.

**Class method** (`@classmethod`): receives the class itself (`cls`) as
first argument, typically used as an alternative constructor.
```python
    @classmethod
    def anonymous(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0)
```
`Plant.anonymous()` builds a plant without needing details. (Return type is
a string `"Plant"` because the class isn't fully defined yet inside its own
body.) Note it only works as-is for `Plant` itself: subclasses have a
different `__init__` signature.

**Nested class**: `Plant.Stats` is defined inside `Plant`:
```python
    class Stats:
        def __init__(self) -> None:
            self._grow_calls: int = 0
            self._age_calls: int = 0
            self._show_calls: int = 0
        def count_grow(self): ...
        def display(self) -> None:
            print(f"Stats: {self._grow_calls} grow, ...")
```
Counters are protected (encapsulation) and only changed through
`count_*` methods; `display()` prints them. Each plant creates its own
`Plant.Stats()` in `__init__` (`self._stats`), and `show()`, `grow()`,
`age()` each call the matching `count_*` first. Because `Flower.show()`
calls `super().show()` exactly once, one `show()` counts as one.

**Seed(Flower)** is an inheritance *chain*: Seed to Flower to Plant.
`bloom()` calls `super().bloom()` and then sets `_seeds = 42`; `show()` calls
the Flower's show and appends `Seeds: n`.

**Tree statistics**: Trees need one more counter, so
```python
    class TreeStats(Plant.Stats):
        def __init__(self) -> None:
            super().__init__()
            self._shade_calls: int = 0
        def display(self) -> None:
            super().display()
            print(f" {self._shade_calls} shade")
```
extends the base stats class. In `Tree.__init__` we keep a typed reference
`self._tree_stats` (so we can call `count_shade()`) and also assign it to
`self._stats`, replacing the generic one, so the inherited `grow/age/show`
now count into the extended object too.

**The standalone function**
```python
def display_stats(plant: Plant) -> None:
    print(f"[statistics for {plant.get_name()}]")
    plant.get_stats().display()
```
Not in any class; works for any plant because every kind of plant is a
`Plant` and `display()` is **polymorphic**: for a Tree it calls
`TreeStats.display`, for others `Stats.display`, with no `if` on the type.

The demo values (`Rose` growth rate 8.0, `Sunflower` rate 30.0 with `age(20)`)
are picked so your output reproduces the sample numbers exactly (23.0cm,
110.0cm / 65 days).

---
# Things evaluators like to ask

1. `@staticmethod` vs `@classmethod` vs a normal method?
2. What does `super()` do, and why not copy the parent's code?
3. Why `_x` and not `__x` here? (convention vs name mangling)
