import re
from typing import Any

from app.tools.base import NormalizedResult, ResultType, ToolAdapter

_LINE_RE = re.compile(r"^(\S+)\s+\(Status:\s*(\d+)\)(?:\s+\[Size:\s*(\d+)\])?")

DEFAULT_WORDLIST = "/home/scanner/wordlists/common.txt"


class GobusterAdapter(ToolAdapter):
    name = "gobuster"

    def build_command(self, params: dict[str, Any]) -> list[str]:
        url = params["url"]
        wordlist = params.get("wordlist", DEFAULT_WORDLIST)
        return ["gobuster", "dir", "-u", url, "-w", wordlist, "-q", "--no-error"]

    def parse_output(self, stdout: str, stderr: str) -> list[NormalizedResult]:
        results = []
        for line in stdout.splitlines():
            line = line.strip()
            match = _LINE_RE.match(line)
            if not match:
                continue
            path, status, size = match.groups()
            results.append(
                NormalizedResult(
                    type=ResultType.url,
                    value=path,
                    raw={"status": int(status), "size": int(size) if size else None, "line": line},
                )
            )
        return results
