from math import ceil

from app.schemas.tools import (
    Difficulty,
    EstimateLearningEffortRequest,
    EstimateLearningEffortResponse,
)

# Horas base por tema (nivel "baja")
BASE_HOURS_PER_TOPIC: float = 1.5

# Multiplicador por dificultad
DIFFICULTY_FACTOR: dict[Difficulty, float] = {
    Difficulty.BAJA: 1.0,
    Difficulty.MEDIA: 1.5,
    Difficulty.ALTA: 2.0,
}


def estimate_learning_effort(
    request: EstimateLearningEffortRequest,
) -> EstimateLearningEffortResponse:
    """Estima el esfuerzo para completar una actividad formativa.

    Regla de negocio:
        total_horas   = temas * 1.5 * factor_dificultad
        semanas       = total_horas / horas_semanales_disponibles
        dias          = ceil(semanas * 7)
    """
    base_hours = request.topics_count * BASE_HOURS_PER_TOPIC
    factor = DIFFICULTY_FACTOR[request.difficulty]
    total_hours = round(base_hours * factor, 2)

    raw_weeks = total_hours / request.weekly_hours_available
    estimated_weeks = round(raw_weeks, 2)
    estimated_days = max(1, ceil(raw_weeks * 7))

    if estimated_weeks <= 1:
        recommendation = "Plan intensivo: cabe en una semana."
    elif estimated_weeks <= 4:
        recommendation = "Plan mensual: distribúyelo en 4 semanas."
    else:
        recommendation = "Plan extendido: divide en bloques semanales."

    return EstimateLearningEffortResponse(
        activity=request.activity,
        difficulty=request.difficulty,
        total_hours=total_hours,
        estimated_weeks=estimated_weeks,
        estimated_days=estimated_days,
        recommendation=recommendation,
    )