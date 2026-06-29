export function buildToolParams(tool: string, input: string): Record<string, unknown> {
  const trimmed = input.trim()
  switch (tool) {
    case 'subfinder':
      return { domain: trimmed }
    case 'nmap':
      return { target: trimmed }
    case 'gobuster':
    case 'whatweb':
    case 'ffuf':
      return { url: trimmed }
    default:
      return { targets: input.split('\n').map((l) => l.trim()).filter(Boolean) }
  }
}

export function toolInputPlaceholder(tool: string): string {
  switch (tool) {
    case 'subfinder':
      return 'dominio, ej. example.com'
    case 'nmap':
      return 'host o IP, ej. example.com'
    case 'gobuster':
    case 'whatweb':
      return 'url, ej. https://example.com'
    case 'ffuf':
      return 'url con FUZZ, ej. https://example.com/FUZZ'
    default:
      return 'targets (uno por línea), ej. https://example.com'
  }
}
