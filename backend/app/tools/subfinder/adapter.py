import json
from typing import Any

from app.tools.base import NormalizedResult, ResultType, ToolAdapter


class SubfinderAdapter(ToolAdapter):
    name = "subfinder"

    def build_command(self, params: dict[str, Any]) -> list[str]:
        domain = params["domain"]
        return ["subfinder", "-d", domain, "-silent", "-json"]

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
