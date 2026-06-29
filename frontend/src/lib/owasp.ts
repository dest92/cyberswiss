export const OWASP_TOP_10: Array<{ code: string; name: string }> = [
  { code: 'A01:2021', name: 'Broken Access Control' },
  { code: 'A02:2021', name: 'Cryptographic Failures' },
  { code: 'A03:2021', name: 'Injection' },
  { code: 'A04:2021', name: 'Insecure Design' },
  { code: 'A05:2021', name: 'Security Misconfiguration' },
  { code: 'A06:2021', name: 'Vulnerable and Outdated Components' },
  { code: 'A07:2021', name: 'Identification and Authentication Failures' },
  { code: 'A08:2021', name: 'Software and Data Integrity Failures' },
  { code: 'A09:2021', name: 'Security Logging and Monitoring Failures' },
  { code: 'A10:2021', name: 'Server-Side Request Forgery (SSRF)' },
]

export const OWASP_CODES = OWASP_TOP_10.map((c) => c.code)
