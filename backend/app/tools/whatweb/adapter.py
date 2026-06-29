import json
from typing import Any

from app.tools.base import NormalizedResult, ResultType, ToolAdapter


class WhatWebAdapter(ToolAdapter):
    name = "whatweb"

    def build_command(self, params: dict[str, Any]) -> list[str]:
        url = params["url"]
        return ["whatweb", "--no-errors", "-a", "1", "--log-json=-", url]

    def parse_output(self, stdout: str, stderr: str) -> list[NormalizedResult]:
        entries = self._parse_entries(stdout)
        results = []
        for data in entries:
            target = data.get("target")
            if not target:
                continue
            results.append(
                NormalizedResult(
                    type=ResultType.finding,
                    value=target,
                    raw=data.get("plugins", {}),
                )
            )
        return results

    def _parse_entries(self, stdout: str) -> list[dict[str, Any]]:
        stripped = stdout.strip()
        if not stripped:
            return []

        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError:
            pass
        else:
            if isinstance(parsed, list):
                return [entry for entry in parsed if isinstance(entry, dict)]
            if isinstance(parsed, dict):
                return [parsed]

        entries = []
        for line in stripped.splitlines():
            line = line.strip().rstrip(",")
            if not line.startswith("{"):
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            entries.append(data)
        return entries
