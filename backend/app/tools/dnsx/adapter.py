import json
from typing import Any

from app.tools.base import NormalizedResult, ResultType, ToolAdapter


class DnsxAdapter(ToolAdapter):
    """Adapter para `dnsx` de ProjectDiscovery: resuelve una lista de hosts/subdominios
    y descarta los que no responden, antes de pasarlos a herramientas de probing HTTP."""

    name = "dnsx"

    def build_command(self, params: dict[str, Any]) -> list[str]:
        return ["dnsx", "-silent", "-json", "-no-color", "-a", "-resp"]

    def build_stdin(self, params: dict[str, Any]) -> bytes | None:
        targets: list[str] = params.get("targets", [])
        return ("\n".join(targets) + "\n").encode("utf-8")

    def parse_output(self, stdout: str, stderr: str) -> list[NormalizedResult]:
        results = []
        for line in stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            host = data.get("host")
            if host:
                results.append(NormalizedResult(type=ResultType.host, value=host, raw=data))
        return results
