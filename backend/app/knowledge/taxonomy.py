"""Taxonomía OWASP Top 10 (2021), usada como clasificación principal de findings
y como estructura de la biblioteca de conocimiento."""

OWASP_TOP_10 = [
    ("A01:2021", "Broken Access Control"),
    ("A02:2021", "Cryptographic Failures"),
    ("A03:2021", "Injection"),
    ("A04:2021", "Insecure Design"),
    ("A05:2021", "Security Misconfiguration"),
    ("A06:2021", "Vulnerable and Outdated Components"),
    ("A07:2021", "Identification and Authentication Failures"),
    ("A08:2021", "Software and Data Integrity Failures"),
    ("A09:2021", "Security Logging and Monitoring Failures"),
    ("A10:2021", "Server-Side Request Forgery (SSRF)"),
]

OWASP_CODES = [code for code, _ in OWASP_TOP_10]
