from abc import ABC, abstractmethod
from typing import Any, Protocol


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


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CsvExportPlugin:
    @staticmethod
    def _csv_field(value: str) -> str:
        if any(char in value for char in (",", '"', "\n")):
            return '"' + value.replace('"', '""') + '"'
        return value

    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        print(",".join(self._csv_field(value) for _, value in data))


class JsonExportPlugin:
    @staticmethod
    def _json_string(value: str) -> str:
        escaped: str = (value.replace("\\", "\\\\")
                        .replace('"', '\\"')
                        .replace("\n", "\\n")
                        .replace("\r", "\\r")
                        .replace("\t", "\\t"))
        return '"' + escaped + '"'

    def process_output(self, data: list[tuple[int, str]]) -> None:
        pairs: list[str] = [
            f'"item_{rank}": {self._json_string(value)}'
            for rank, value in data]
        print("JSON Output:")
        print("{" + ", ".join(pairs) + "}")


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    break
            else:
                print("DataStream error - Can't process element in "
                      f"stream: {element}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            print(f"{proc.name}: total {proc.total_processed} items "
                  f"processed, remaining {proc.remaining} on processor")

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._processors:
            count: int = min(nb, proc.remaining)
            if count == 0:
                continue
            batch: list[tuple[int, str]] = [
                proc.output() for _ in range(count)]
            plugin.process_output(batch)


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("Registering Processors")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    first: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [{"log_level": "WARNING",
          "log_message": "Telnet access! Use ssh instead"},
         {"log_level": "INFO", "log_message": "User wil is connected"}],
        42,
        ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {first}")
    stream.process_stream(first)
    stream.print_processors_stats()

    print("Send 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CsvExportPlugin())
    stream.print_processors_stats()

    second: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [{"log_level": "ERROR", "log_message": "500 server crash"},
         {"log_level": "NOTICE",
          "log_message": "Certificate expires in 10 days"}],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"Send another batch of data: {second}")
    stream.process_stream(second)
    stream.print_processors_stats()

    print("Send 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JsonExportPlugin())
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
