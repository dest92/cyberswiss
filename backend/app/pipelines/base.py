from dataclasses import dataclass
from typing import Any, Callable

from app.tools.base import NormalizedResult

BuildParams = Callable[[dict[str, Any], list[NormalizedResult]], dict[str, Any]]


@dataclass
class PipelineStep:
    """Un paso de un pipeline: qué herramienta corre y cómo construir sus
    params a partir del input original y los resultados del paso anterior."""

    tool_name: str
    build_params: BuildParams


@dataclass
class PipelineDefinition:
    name: str
    steps: list[PipelineStep]
