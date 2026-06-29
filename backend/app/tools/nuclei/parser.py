"""Mapeo best-effort de tags de templates de nuclei a categorías OWASP Top 10 (2021).

No es exhaustivo: cubre los tags más comunes en templates web. Sirve para
auto-clasificar findings derivados de nuclei; el usuario puede corregir la
categoría manualmente en el finding generado.
"""

NUCLEI_TAG_TO_OWASP: dict[str, str] = {
    # A01: Broken Access Control
    "idor": "A01:2021",
    "broken-access": "A01:2021",
    "privilege-escalation": "A01:2021",
    "traversal": "A01:2021",
    "redirect": "A01:2021",
    "lfi": "A01:2021",
    "access-control": "A01:2021",
    # A02: Cryptographic Failures
    "exposure": "A02:2021",
    "exposed-token": "A02:2021",
    "secrets": "A02:2021",
    "apikey": "A02:2021",
    "tls": "A02:2021",
    "ssl": "A02:2021",
    # A03: Injection
    "sqli": "A03:2021",
    "xss": "A03:2021",
    "rce": "A03:2021",
    "ssti": "A03:2021",
    "xxe": "A03:2021",
    "injection": "A03:2021",
    "command-injection": "A03:2021",
    # A05: Security Misconfiguration
    "exposed-panel": "A05:2021",
    "exposed-db": "A05:2021",
    "misconfig": "A05:2021",
    "default-config": "A05:2021",
    "debug": "A05:2021",
    "takeover": "A05:2021",
    "subdomain-takeover": "A05:2021",
    # A06: Vulnerable and Outdated Components
    "cve": "A06:2021",
    "outdated-version": "A06:2021",
    "tech": "A06:2021",
    "wordpress": "A06:2021",
    "log4j": "A06:2021",
    # A07: Identification and Authentication Failures
    "default-login": "A07:2021",
    "weak-login": "A07:2021",
    "auth-bypass": "A07:2021",
    "jwt": "A07:2021",
    "auth": "A07:2021",
    # A08: Software and Data Integrity Failures
    "deserialization": "A08:2021",
    # A10: SSRF
    "ssrf": "A10:2021",
}


def classify_owasp(tags: list[str]) -> str | None:
    for tag in tags:
        category = NUCLEI_TAG_TO_OWASP.get(tag.lower())
        if category:
            return category
    return None
