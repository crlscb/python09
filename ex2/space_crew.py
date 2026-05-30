from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError


class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


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
    def mission_validation(self) -> "SpaceMission":

        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with M")

        has_leader = False

        for member in self.crew:
            if (
                member.rank == Rank.commander
                or member.rank == Rank.captain
            ):
                has_leader = True

        if not has_leader:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
                )

        experienced_crew = 0

        for member in self.crew:
            if member.years_experience >= 5:
                experienced_crew += 1

        if self.duration_days > 365:
            if experienced_crew < len(self.crew) / 2:
                raise ValueError(
                    "Long missions need 50% experienced crew"
                )

        for member in self.crew:
            if not member.is_active:
                raise ValueError(
                    "All crew members must be active"
                )

        return self


def main() -> None:
    commander = CrewMember(
        member_id="CM001",
        name="Sarah Connor",
        rank=Rank.commander,
        age=45,
        specialization="Mission Command",
        years_experience=15
    )

    lieutenant = CrewMember(
        member_id="CM002",
        name="John Smith",
        rank=Rank.lieutenant,
        age=35,
        specialization="Navigation",
        years_experience=8
    )

    officer = CrewMember(
        member_id="CM003",
        name="Alice Johnson",
        rank=Rank.officer,
        age=33,
        specialization="Engineering",
        years_experience=6
    )

    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime.fromisoformat(
            "2026-01-12T14:23:00"
        ),
        duration_days=900,
        crew=[commander, lieutenant, officer],
        budget_millions=2500.0
    )

    print("Space Mission Crew Validation")
    print("=========================================")
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    for member in mission.crew:
        print(
            f"- {member.name} "
            f"({member.rank.value})"
            f" - ({member.specialization})"
        )

    print()
    print("=========================================")
    try:
        cadet = CrewMember(
            member_id="CM001",
            name="Emma Connor",
            rank=Rank.cadet,
            age=27,
            specialization="Cadet",
            years_experience=3
        )

        lieutenant = CrewMember(
            member_id="CM002",
            name="John Smith",
            rank=Rank.lieutenant,
            age=35,
            specialization="Navigation",
            years_experience=8
        )

        officer = CrewMember(
            member_id="CM003",
            name="Alice Johnson",
            rank=Rank.officer,
            age=33,
            specialization="Engineering",
            years_experience=6
        )

        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.fromisoformat(
                "2026-01-12T14:23:00"
            ),
            duration_days=900,
            crew=[cadet, lieutenant, officer],
            budget_millions=2500.0
        )

    except ValidationError as error:
        print("Expected validation error:")
        print(
            error.errors()[0]["msg"].replace(
                "Value error, ",
                ""
            )
        )


if __name__ == "__main__":
    main()
