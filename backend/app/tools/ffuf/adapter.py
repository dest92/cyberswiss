from typing import Any

from app.tools.base import NormalizedResult, ResultType, ToolAdapter

DEFAULT_WORDLIST = "/home/scanner/wordlists/common.txt"


class FfufAdapter(ToolAdapter):
    """Fuzzing genérico: el caller debe incluir el literal `FUZZ` en la url donde
    quiera sustituir cada palabra del wordlist (path, parámetro, header, etc.)."""

    name = "ffuf"

    def build_command(self, params: dict[str, Any]) -> list[str]:
        url = params["url"]
        wordlist = params.get("wordlist", DEFAULT_WORDLIST)
        return ["ffuf", "-u", url, "-w", wordlist, "-s"]

    def parse_output(self, stdout: str, stderr: str) -> list[NormalizedResult]:
        results = []
        for line in stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            results.append(
                NormalizedResult(type=ResultType.finding, value=line, raw={"matched": line})
            )
        return results
