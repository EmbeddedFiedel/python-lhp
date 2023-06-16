# Python: Asynchronous client for the Länderübergreifendes Hochwasserportal (LHP) API.
from __future__ import annotations

from pydantic import BaseModel, Field

from .util import StrEnum



class PrecipitationUnit(StrEnum):
    """Enum to represent the precipitation units available."""

    CENTIMETERS = "cm"
    INCHES = "in"


class CurrentWaterLevel(BaseModel):
    """Current weather data."""

    water_level: float = Field(..., alias="W_float")
    flood: int = Field(..., alias="HW")
    flood_text: str = Field(..., alias="HW_TXT")
