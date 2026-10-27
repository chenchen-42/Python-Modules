from datetime import datetime

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def first_error_message(error: ValidationError) -> str:
    message: str = str(error.errors()[0]["msg"])
    return message.removeprefix("Value error, ")


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)

    # last_maintenance is a plain string: Pydantic converts it to datetime
    valid_data: dict[str, object] = {
        "station_id": "ISS001",
        "name": "International Space Station",
        "crew_size": 6,
        "power_level": 85.5,
        "oxygen_level": 92.3,
        "last_maintenance": "2024-01-15T10:30:00",
    }
    try:
        station: SpaceStation = SpaceStation.model_validate(valid_data)
        status: str = "Operational" if station.is_operational else "Offline"
        print("Valid station created:")
        print(f"ID: {station.station_id}")
        print(f"Name: {station.name}")
        print(f"Crew: {station.crew_size} people")
        print(f"Power: {station.power_level}%")
        print(f"Oxygen: {station.oxygen_level}%")
        print(f"Status: {status}")
        print(f"Last maintenance: {station.last_maintenance} "
              f"({type(station.last_maintenance).__name__})")
    except ValidationError as error:
        print(f"Unexpected validation error: {first_error_message(error)}")

    print()
    print("=" * 40)
    invalid_data: dict[str, object] = dict(valid_data, crew_size=25)
    try:
        SpaceStation.model_validate(invalid_data)
        print("Invalid station was accepted (this should not happen)")
    except ValidationError as error:
        print("Expected validation error:")
        print(first_error_message(error))


if __name__ == "__main__":
    main()
