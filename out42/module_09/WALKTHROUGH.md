# Module 09: Cosmic Data (Pydantic models & validation)

Files: `ex0/space_station.py`, `ex1/alien_contact.py`, `ex2/space_crew.py`.
Tested with Python 3.12 and Pydantic 2.14. `flake8` is clean and
`mypy --strict` passes. As before, the goal is that you can rebuild and
explain these yourself in the defense: read, close the file, retype, run,
explain to a peer. **[choice]** marks decisions the subject leaves open.

## Setup (required: venv + pip + Pydantic 2.x)

```bash
python3 -m venv venv
source venv/bin/activate
pip install pydantic flake8 mypy
```
A **virtual environment** is an isolated folder of packages for this
project, so installs don't touch the system Python. Don't commit `venv/`
(add it to `.gitignore`): the subject says to submit only the requested
files.

## The ideas behind Pydantic in 60 seconds

- A **model** is a class that inherits from `BaseModel`. You declare fields
  as annotated class attributes (`crew_size: int`).
- When you build an instance, Pydantic **validates** every field: it checks
  the type and the constraints. If the data is wrong it raises a
  `ValidationError` and no object is created ("data integrity").
- It also **converts** compatible values (**coercion**): the string
  `"2024-01-15T10:30:00"` becomes a real `datetime`, `"radio"` becomes the
  `ContactType.RADIO` enum member, the dict `{"name": ...}` becomes a nested
  model. That answers the subject's "Think About" question.
- `Field(...)` attaches constraints: `ge`/`le` (greater/less or equal),
  `gt`/`lt`, `min_length`/`max_length`, `default`.
- `@model_validator(mode="after")` runs **after** all the fields passed their
  checks and sees the whole object through `self`: perfect for rules that
  involve several fields. It must `return self`. (Pydantic v1's `@validator`
  is deprecated; the subject forbids it.)

---
## ex0: space_station.py

```python
from datetime import datetime

from pydantic import BaseModel, Field, ValidationError
```
`datetime` is the standard-library type for date+time. From Pydantic we need
the base class, `Field` for constraints, and `ValidationError`, the exception
raised on bad data. (Two import groups, stdlib then third-party, separated
by a blank line: flake8/PEP 8 style.)

```python
class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)
```
Field by field, matching the subject:
- `station_id: str = Field(min_length=3, max_length=10)`: the annotation
  `str` is the type; `Field(...)` adds the 3-10 length rule.
- `crew_size: int = Field(ge=1, le=20)`: `ge=1` means "greater than or equal
  to 1", `le=20` "less than or equal to 20". The sample error text
  *"Input should be less than or equal to 20"* comes from this `le`.
- `power_level` / `oxygen_level`: floats from 0.0 to 100.0 (percentages).
- `last_maintenance: datetime`: no constraint, so no `Field`. It has **no
  default**, therefore it is **required**.
- `is_operational: bool = True`: a plain default value makes the field
  optional; if omitted it is `True`.
- `notes: str | None = Field(default=None, max_length=200)`: `str | None`
  means "a string or None"; `default=None` makes it optional;
  `max_length=200` only applies when a string is given.

```python
def first_error_message(error: ValidationError) -> str:
    message: str = str(error.errors()[0]["msg"])
    return message.removeprefix("Value error, ")
```
`error.errors()` is a list of dicts, one per problem, each with keys like
`loc` (where), `msg` (human text) and `type`. We take the first one's `msg`.
`removeprefix` strips the `"Value error, "` that Pydantic prepends to
messages coming from our own `raise ValueError(...)` in custom validators
(used from ex1 on; here it does nothing). The helper keeps the output
identical to the sample.

```python
def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)
```
`"=" * 40` repeats the character 40 times: the separator line.

```python
    valid_data: dict[str, object] = {
        "station_id": "ISS001",
        ...
        "last_maintenance": "2024-01-15T10:30:00",
    }
    try:
        station: SpaceStation = SpaceStation.model_validate(valid_data)
```
The data is a plain dict, like what you'd get from JSON, and
`last_maintenance` is deliberately a **string**.
`SpaceStation.model_validate(dict)` is the Pydantic v2 way to validate a dict
(`SpaceStation(**dict)` also works). It converts the ISO string to a
`datetime`: the last print line shows `(datetime)`. The dict is typed
`dict[str, object]` so mypy doesn't complain about a str in a datetime field.

```python
        status: str = "Operational" if station.is_operational else "Offline"
        print("Valid station created:")
        ...
        print(f"Power: {station.power_level}%")
```
A conditional expression picks the status text. Each field is read as a
normal attribute (`station.crew_size`) and it already has the right Python
type. The `except ValidationError` branch exists so the demo never crashes
if the "valid" data were wrong.

```python
    invalid_data: dict[str, object] = dict(valid_data, crew_size=25)
    try:
        SpaceStation.model_validate(invalid_data)
        print("Invalid station was accepted (this should not happen)")
    except ValidationError as error:
        print("Expected validation error:")
        print(first_error_message(error))
```
`dict(valid_data, crew_size=25)` copies the dict and overrides one key: all
valid except `crew_size > 20`. Validation fails, **no object is created**,
and we print the message.

---
## ex1: alien_contact.py

```python
class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"
```
An **Enum** is a fixed set of allowed values. Inheriting from `str` too makes
the members behave as strings (handy for JSON). Pydantic accepts either the
member or its value: `"radio"` becomes `ContactType.RADIO`; `"banana"` gives
a validation error automatically, with no code from you. `.value` gives
back the plain string (`"radio"`).

```python
class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    ...
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False
```
Same techniques as ex0, with the ranges from the subject (1440 minutes = 24
hours). `contact_type: ContactType` uses the enum as the type.

```python
    @model_validator(mode="after")
    def check_business_rules(self) -> "AlienContact":
```
- `@model_validator(mode="after")` registers the method to run after the
  field checks, so every `self.x` is already valid and correctly typed.
- The return annotation is a **string** `"AlienContact"` because the class
  isn't finished being defined yet at that point (forward reference).

```python
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')
```
`startswith` is a str method. To reject data inside a validator you
`raise ValueError(...)`; Pydantic catches it and turns it into a
`ValidationError` whose message is `"Value error, <your text>"`, which is
what `first_error_message` cleans.

```python
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if (self.contact_type == ContactType.TELEPATHIC
                and self.witness_count < 3):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses")
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) must include a message")
        return self
```
The business rules in order. Parentheses let the `if` span two lines.
**[choice]** the subject says strong signals "should" include a message; I
treat it as required (an empty or missing message fails), because a
validator can only accept or reject. `not self.message_received` is true for
both `None` and `""`. **`return self` is mandatory**: with `mode="after"`,
the returned value *is* the validated object.

```python
def build_report(**changes: object) -> AlienContact:
    data: dict[str, object] = {... a valid report ...}
    data.update(changes)
    return AlienContact.model_validate(data)
```
A test helper: start from a valid report and override some fields.
`**changes` collects keyword arguments into a dict, `update` merges them.
It keeps the demo short and shows which single change breaks which rule.

`main()`: builds the valid report and prints it (`contact.contact_type.value`
gives `radio`); then a telepathic contact with 2 witnesses and a weak signal
(5.0, so that the "strong signal" rule isn't the one that triggers first)
produces the sample error. The final loop uses `build_report(**changes)` with
a dict of changes (`**` unpacks a dict into keyword arguments) to show the
three other rules failing, one by one.

**Order matters:** after-validators raise at the *first* broken rule, so one
report shows only one message at a time.

---
## ex2: space_crew.py

`Rank` is an Enum exactly like `ContactType`.

`CrewMember` is a normal model: ranges for `age` (18-80),
`years_experience` (0-50), and `is_active: bool = True`.

```python
class SpaceMission(BaseModel):
    ...
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)
```
**Nested model**: `crew: list[CrewMember]` means "a list where every item
is a valid `CrewMember`". Pydantic validates each member with the
`CrewMember` rules, and accepts either `CrewMember` objects or plain dicts
(it converts them). On a list, `min_length`/`max_length` constrain the number
of items (1-12 members).

**What happens when a nested member is invalid?** The whole mission fails
validation, and the error points to the exact place. The last block of
`main()` demonstrates it with a 15-year-old commander: the error location is
`crew -> 0 -> age` (field `crew`, item 0, field `age`) with message
*"Input should be greater than or equal to 18"*. Also important: field
validation happens **first**; the `after` validator never runs on a
mission whose crew is invalid.

```python
    @model_validator(mode="after")
    def check_safety_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')
```
Rule 1.

```python
        leaders: list[CrewMember] = [
            member for member in self.crew
            if member.rank in (Rank.COMMANDER, Rank.CAPTAIN)
        ]
        if not leaders:
            raise ValueError(
                "Mission must have at least one Commander or Captain")
```
Rule 2. A **list comprehension** keeps only members whose rank is in the
tuple `(COMMANDER, CAPTAIN)` (`in` tests membership). An empty list is
"falsy", so `not leaders` means "no commander/captain at all".

```python
        if self.duration_days > 365:
            veterans: int = sum(
                1 for member in self.crew if member.years_experience >= 5)
            if veterans * 2 < len(self.crew):
                raise ValueError(
                    "Long missions (> 365 days) need at least 50% "
                    "experienced crew (5+ years)")
```
Rule 3, only for long missions. `sum(1 for ... if ...)` counts members with 5+
years (a generator that yields 1 per match). "At least 50%" means
`veterans / total >= 0.5`; written as `veterans * 2 >= total` it avoids float
division, so the failure condition is `veterans * 2 < total`. Example: in
the valid mission, 2 of 3 are veterans, so `4 < 3` is false and it passes;
with 1 of 3, `2 < 3` is true and it fails.

```python
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self
```
Rule 4. `all(...)` is `True` only if every item is true. Then `return self`.

Helpers `make_crew_member` and `make_mission` build objects with keyword
arguments so the demo reads clearly. In `main()` the valid mission mirrors
the sample (Sarah Connor, John Smith, Alice Johnson). The invalid one has
no Commander or Captain and a short duration (100 days), so the experience
rule can't be the one that fires first. Then each remaining rule is
triggered in turn, and finally the nested-error demo. Note
`inactive.is_active = False` mutates a model after creation: Pydantic does
**not** re-validate on assignment by default, which is why that object can
be built and then marked inactive.

---
## Questions to prepare for the defense

1. Why `Field(...)` for constraints but a bare default (`= True`) for simple
   defaults? (`Field` carries rules and metadata; a bare value is just the
   default.)
2. Validation vs coercion: what does Pydantic convert, and what does it reject?
   (In default "lax" mode: `"25"` becomes `25`, but `"abc"` for an int fails.)
3. Why use `mode="after"` and why `return self`?
4. `@model_validator` vs a field-level check: when do you need the whole
   model? (rules that compare several fields)
5. What does a `ValidationError` contain, and how do you read it? (`errors()`:
   `loc`, `msg`, `type`)
6. What happens to a nested model that fails? (the parent fails too, with
   the error path)
7. Why is `str | None` different from a field with a default of `None`?
   (the first says the value may be None; the second says it may be omitted.
   `notes` has both)
8. Why can't Pydantic stop you from assigning `is_active = False` later?
   (validation runs at construction unless you enable
   `validate_assignment`)
