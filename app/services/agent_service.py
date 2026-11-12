from typing import Any

from pydantic import BaseModel, ValidationError

from app.tools.registry import REGISTRY


class ToolNotFoundError(Exception):
    pass


class ToolExecutionError(Exception):
    pass


class AgentService:
    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> BaseModel:
        spec = REGISTRY.get(tool_name)
        if spec is None:
            raise ToolNotFoundError(
                f"Herramienta '{tool_name}' no registrada. "
                f"Disponibles: {sorted(REGISTRY)}"
            )

        try:
            args = spec.args_model.model_validate(arguments)
        except ValidationError as exc:
            raise ToolExecutionError(
                f"Argumentos inválidos para '{tool_name}': {exc}"
            ) from exc

        return spec.handler(args)