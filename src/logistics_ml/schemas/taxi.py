from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaxiTripEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    trip_id: str

    pickup_zone: int = Field(ge=1)
    dropoff_zone: int = Field(ge=1)

    distance_km: float = Field(gt=0)

    passengers: int = Field(ge=1)

    timestamp: datetime
