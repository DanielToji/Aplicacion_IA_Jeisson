from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Difficulty(str, Enum):
    """Niveles permitidos. Hereda de str para serializar como string en JSON."""
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"


class EstimateLearningEffortRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,  # "  FastAPI  " → "FastAPI"
        json_schema_extra={
            "examples": [
                {
                    "activity": "Curso de FastAPI",
                    "difficulty": "media",
                    "topics_count": 5,
                    "weekly_hours_available": 10.0,
                }
            ]
        },
    )

    activity: str = Field(
        min_length=3,
        max_length=200,
        examples=["Curso de FastAPI"],
    )
    difficulty: Difficulty = Field(examples=["media"])
    topics_count: int = Field(ge=1, le=50, examples=[5])
    weekly_hours_available: float = Field(gt=0, le=40, examples=[10.0])


class EstimateLearningEffortResponse(BaseModel):
    activity: str
    difficulty: Difficulty
    total_hours: float
    estimated_weeks: float
    estimated_days: int
    recommendation: str