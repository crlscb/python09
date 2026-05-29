from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, model_validator


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
        
        experienced_crew  = 0

        for member in self.crew:
            if member.years_experience >= 5:
                experienced_crew  += 1
        
        if self.duration_days > 365:
            if experienced_crew  < len(self.crew) / 2:
                raise ValueError(
                    "Long missions need 50% experienced crew"
                )
        
        for member in self.crew:
            if not member.is_active:
                raise ValueError(
                    "All crew members must be active"
                )

        return self
