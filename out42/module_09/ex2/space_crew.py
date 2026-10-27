from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_safety_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        leaders: list[CrewMember] = [
            member for member in self.crew
            if member.rank in (Rank.COMMANDER, Rank.CAPTAIN)
        ]
        if not leaders:
            raise ValueError(
                "Mission must have at least one Commander or Captain")

        if self.duration_days > 365:
            veterans: int = sum(
                1 for member in self.crew if member.years_experience >= 5)
            if veterans * 2 < len(self.crew):
                raise ValueError(
                    "Long missions (> 365 days) need at least 50% "
                    "experienced crew (5+ years)")

        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self


def first_error_message(error: ValidationError) -> str:
    message: str = str(error.errors()[0]["msg"])
    return message.removeprefix("Value error, ")


def make_crew_member(member_id: str, name: str, rank: Rank,
                     specialization: str, years: int,
                     age: int = 40) -> CrewMember:
    return CrewMember(member_id=member_id, name=name, rank=rank, age=age,
                      specialization=specialization,
                      years_experience=years)


def make_mission(crew: list[CrewMember], mission_id: str = "M2024_MARS",
                 duration_days: int = 900) -> SpaceMission:
    return SpaceMission(
        mission_id=mission_id,
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2025, 3, 1),
        duration_days=duration_days,
        crew=crew,
        budget_millions=2500.0,
    )


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 41)

    crew: list[CrewMember] = [
        make_crew_member("CM001", "Sarah Connor", Rank.COMMANDER,
                         "Mission Command", 15, 45),
        make_crew_member("CM002", "John Smith", Rank.LIEUTENANT,
                         "Navigation", 8, 38),
        make_crew_member("CM003", "Alice Johnson", Rank.OFFICER,
                         "Engineering", 3, 31),
    ]
    mission: SpaceMission = make_mission(crew)
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(f"- {member.name} ({member.rank.value}) - "
              f"{member.specialization}")

    print()
    print("=" * 41)
    try:
        make_mission([
            make_crew_member("CM004", "Bob Stone", Rank.OFFICER,
                             "Engineering", 10),
            make_crew_member("CM005", "Eve Park", Rank.CADET,
                             "Biology", 1, 25),
        ], duration_days=100)
    except ValidationError as error:
        print("Expected validation error:")
        print(first_error_message(error))

    print()
    print("Other safety rules:")
    inactive: CrewMember = make_crew_member(
        "CM006", "Ann Lee", Rank.CAPTAIN, "Command", 10)
    inactive.is_active = False
    rule_tests: list[tuple[str, list[CrewMember], str, int]] = [
        ("bad ID", crew, "X2024_MARS", 900),
        ("too few veterans", [crew[0], crew[2],
                              make_crew_member("CM007", "Tim Roe",
                                               Rank.CADET, "Medicine", 1)],
         "M2024_MARS", 900),
        ("inactive member", [inactive], "M2024_MARS", 100),
    ]
    for label, members, mission_id, days in rule_tests:
        try:
            make_mission(members, mission_id, days)
        except ValidationError as error:
            print(f"- {label}: {first_error_message(error)}")

    print()
    print("Nested validation (a crew member breaks the rules):")
    bad_data: dict[str, object] = {
        "mission_id": "M2024_MARS",
        "mission_name": "Mars Colony Establishment",
        "destination": "Mars",
        "launch_date": "2025-03-01",
        "duration_days": 900,
        "budget_millions": 2500.0,
        "crew": [{"member_id": "CM001", "name": "Kid Pilot",
                  "rank": "commander", "age": 15,
                  "specialization": "Piloting", "years_experience": 0}],
    }
    try:
        SpaceMission.model_validate(bad_data)
    except ValidationError as error:
        first = error.errors()[0]
        location: str = " -> ".join(str(part) for part in first["loc"])
        print(f"- error located at: {location}")
        print(f"- {first['msg']}")


if __name__ == "__main__":
    main()
