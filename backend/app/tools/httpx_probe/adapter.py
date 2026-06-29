import json
from typing import Any

from app.tools.base import NormalizedResult, ResultType, ToolAdapter


class HttpxProbeAdapter(ToolAdapter):
    """Adapter para la herramienta CLI `httpx` de ProjectDiscovery (probing HTTP), no el
    cliente HTTP de Python con el mismo nombre."""

    name = "httpx"

    def build_command(self, params: dict[str, Any]) -> list[str]:
        return ["httpx", "-silent", "-json", "-no-color"]

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
            url = data.get("url") or data.get("input")
            if url:
                results.append(NormalizedResult(type=ResultType.url, value=url, raw=data))
        return results
