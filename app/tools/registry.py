from dataclasses import dataclass
from typing import Any, Callable

from pydantic import BaseModel

from app.schemas.tools import EstimateLearningEffortRequest
from app.tools.estimate_learning_effort import estimate_learning_effort


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    args_model: type[BaseModel]
    handler: Callable[..., BaseModel]


REGISTRY: dict[str, ToolSpec] = {
    "estimate_learning_effort": ToolSpec(
        name="estimate_learning_effort",
        description=(
            "Estima horas, semanas y días para completar una "
            "actividad formativa según dificultad, cantidad de temas "
            "y horas semanales disponibles."
        ),
        args_model=EstimateLearningEffortRequest,
        handler=estimate_learning_effort,
    ),
}