import enum
from abc import ABC, abstractmethod
from typing import Any, ClassVar

from pydantic import BaseModel


class ResultType(str, enum.Enum):
    host = "host"
    url = "url"
    finding = "finding"


class NormalizedResult(BaseModel):
    type: ResultType
    value: str
    raw: dict[str, Any] = {}
    severity: str | None = None
    owasp_category: str | None = None


class ToolAdapter(ABC):
    """Contrato común para integrar una herramienta de línea de comandos.

    Cada adapter solo conoce cómo construir su propio comando y cómo
    normalizar su salida; no conoce a otras herramientas ni al motor de
    ejecución, lo que permite encadenarlas en pipelines sin acoplamiento.
    """

    name: ClassVar[str]

    @abstractmethod
    def build_command(self, params: dict[str, Any]) -> list[str]:
        ...

    def build_stdin(self, params: dict[str, Any]) -> bytes | None:
        return None

    @abstractmethod
    def parse_output(self, stdout: str, stderr: str) -> list[NormalizedResult]:
        ...
