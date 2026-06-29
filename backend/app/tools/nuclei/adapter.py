import json
from typing import Any

from app.tools.base import NormalizedResult, ResultType, ToolAdapter
from app.tools.nuclei.parser import classify_owasp


class NucleiAdapter(ToolAdapter):
    name = "nuclei"

    def build_command(self, params: dict[str, Any]) -> list[str]:
        return [
            "nuclei",
            "-jsonl",
            "-silent",
            "-no-color",
            "-disable-update-check",
            "-l",
            "-",
        ]

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
            info = data.get("info", {})
            tags = info.get("tags", []) or []
            value = data.get("matched-at") or data.get("host") or info.get("name", "unknown")
            results.append(
                NormalizedResult(
                    type=ResultType.finding,
                    value=value,
                    raw=data,
                    severity=info.get("severity"),
                    owasp_category=classify_owasp(tags),
                )
            )
        return results
