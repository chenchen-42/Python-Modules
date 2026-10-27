from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self, name: str) -> None:
        self.name: str = name
        self._queue: list[tuple[int, str]] = []
        self._total: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Tell whether this processor can ingest the given data."""

    @abstractmethod
    def ingest(self, data: Any) -> None:
        """Process the given data (raise ValueError if it is invalid)."""

    def output(self) -> tuple[int, str]:
        if not self._queue:
            raise IndexError(f"{self.name}: no data to output")
        return self._queue.pop(0)

    @property
    def total_processed(self) -> int:
        return self._total

    @property
    def remaining(self) -> int:
        return len(self._queue)

    def _store(self, values: list[str]) -> None:
        for value in values:
            self._queue.append((self._total, value))
            self._total += 1


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Numeric Processor")

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return len(data) > 0 and all(_is_number(item) for item in data)
        return _is_number(data)

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        items: list[int | float] = data if isinstance(data, list) else [data]
        self._store([str(item) for item in items])


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Text Processor")

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return len(data) > 0 and all(isinstance(i, str) for i in data)
        return isinstance(data, str)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        items: list[str] = data if isinstance(data, list) else [data]
        self._store(items)


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Log Processor")

    @staticmethod
    def _is_log(entry: Any) -> bool:
        return isinstance(entry, dict) and len(entry) > 0 and all(
            isinstance(k, str) and isinstance(v, str)
            for k, v in entry.items())

    @staticmethod
    def _to_text(entry: dict[str, str]) -> str:
        if "log_level" in entry and "log_message" in entry:
            return f"{entry['log_level']}: {entry['log_message']}"
        return ", ".join(f"{key}={value}" for key, value in entry.items())

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return len(data) > 0 and all(self._is_log(e) for e in data)
        return self._is_log(data)

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        entries: list[dict[str, str]] = (
            data if isinstance(data, list) else [data])
        self._store([self._to_text(entry) for entry in entries])


def main() -> None:
    print("=== Code Nexus - Data Processor ===")

    print("Testing Numeric Processor...")
    numeric = NumericProcessor()
    for sample in (42, "Hello"):
        print(f"  Trying to validate input '{sample}': "
              f"{numeric.validate(sample)}")
    print("  Test invalid ingestion of string 'foo' without prior "
          "validation:")
    try:
        numeric.ingest("foo")
    except ValueError as error:
        print(f"  Got exception: {error}")
    numbers: list[int | float] = [1, 2, 3, 4, 5]
    print(f"  Processing data: {numbers}")
    numeric.ingest(numbers)
    print("  Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.output()
        print(f"  Numeric value {rank}: {value}")

    print("Testing Text Processor...")
    text = TextProcessor()
    print(f"  Trying to validate input '42': {text.validate(42)}")
    words: list[str] = ["Hello", "Nexus", "World"]
    print(f"  Processing data: {words}")
    text.ingest(words)
    print("  Extracting 1 value...")
    rank, value = text.output()
    print(f"  Text value {rank}: {value}")

    print("Testing Log Processor...")
    logs = LogProcessor()
    print(f"  Trying to validate input 'Hello': {logs.validate('Hello')}")
    entries: list[dict[str, str]] = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f"  Processing data: {entries}")
    logs.ingest(entries)
    print("  Extracting 2 values...")
    for _ in range(2):
        rank, value = logs.output()
        print(f"  Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
