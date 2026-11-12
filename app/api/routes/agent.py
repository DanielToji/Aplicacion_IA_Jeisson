from fastapi import APIRouter, HTTPException

from app.schemas.tools import (
    EstimateLearningEffortRequest,
    EstimateLearningEffortResponse,
)
from app.services.agent_service import AgentService, ToolExecutionError

router = APIRouter(prefix="/api/v1/agent", tags=["agent"])

agent_service = AgentService()


@router.post(
    "/estimate-learning-effort",
    response_model=EstimateLearningEffortResponse,
    summary="Estimar esfuerzo de aprendizaje",
    description=(
        "Calcula horas totales, semanas y días estimados para completar "
        "una actividad formativa, dado su dificultad, cantidad de temas "
        "y horas semanales disponibles."
    ),
)
async def estimate_learning_effort_endpoint(
    payload: EstimateLearningEffortRequest,
) -> EstimateLearningEffortResponse:
    try:
        # model_dump() simula lo que un LLM enviaría como "arguments".
        result = await agent_service.execute(
            "estimate_learning_effort",
            payload.model_dump(),
        )
    except ToolExecutionError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return result  # type: ignore[return-value]