export const MITRE_TECHNIQUES: Array<{ code: string; name: string }> = [
  { code: 'T1190', name: 'Exploit Public-Facing Application' },
  { code: 'T1133', name: 'External Remote Services' },
  { code: 'T1110', name: 'Brute Force' },
  { code: 'T1078', name: 'Valid Accounts' },
  { code: 'T1059', name: 'Command and Scripting Interpreter' },
  { code: 'T1071', name: 'Application Layer Protocol' },
  { code: 'T1040', name: 'Network Sniffing' },
  { code: 'T1046', name: 'Network Service Discovery' },
  { code: 'T1087', name: 'Account Discovery' },
  { code: 'T1083', name: 'File and Directory Discovery' },
  { code: 'T1592', name: 'Gather Victim Host Information' },
  { code: 'T1595', name: 'Active Scanning' },
  { code: 'T1596', name: 'Search Open Technical Databases' },
  { code: 'T1557', name: 'Adversary-in-the-Middle' },
  { code: 'T1552', name: 'Unsecured Credentials' },
  { code: 'T1505', name: 'Server Software Component' },
  { code: 'T1190.001', name: 'Exploit Public-Facing Application: SQL Injection' },
  { code: 'T1199', name: 'Trusted Relationship' },
  { code: 'T1210', name: 'Exploitation of Remote Services' },
  { code: 'T1213', name: 'Data from Information Repositories' },
]

export const MITRE_CODES = MITRE_TECHNIQUES.map((c) => c.code)
