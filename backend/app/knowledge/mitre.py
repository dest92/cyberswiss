"""Catálogo reducido de técnicas MITRE ATT&CK, usado como tagging secundario de
findings (la taxonomía principal sigue siendo OWASP Top 10, ver taxonomy.py).

No es el dataset completo de mitre/cti (seria overkill para un solo usuario):
es un subconjunto curado de técnicas relevantes a recon/web/red team, suficiente
para autocompletar y filtrar en la UI."""

MITRE_TECHNIQUES = [
    ("T1190", "Exploit Public-Facing Application"),
    ("T1133", "External Remote Services"),
    ("T1110", "Brute Force"),
    ("T1078", "Valid Accounts"),
    ("T1059", "Command and Scripting Interpreter"),
    ("T1071", "Application Layer Protocol"),
    ("T1040", "Network Sniffing"),
    ("T1046", "Network Service Discovery"),
    ("T1087", "Account Discovery"),
    ("T1083", "File and Directory Discovery"),
    ("T1592", "Gather Victim Host Information"),
    ("T1595", "Active Scanning"),
    ("T1596", "Search Open Technical Databases"),
    ("T1557", "Adversary-in-the-Middle"),
    ("T1552", "Unsecured Credentials"),
    ("T1505", "Server Software Component"),
    ("T1190.001", "Exploit Public-Facing Application: SQL Injection"),
    ("T1199", "Trusted Relationship"),
    ("T1210", "Exploitation of Remote Services"),
    ("T1213", "Data from Information Repositories"),
]

MITRE_CODES = [code for code, _ in MITRE_TECHNIQUES]
