"""fase 4 findings y knowledge documents

Revision ID: f449f824bb08
Revises: a8913cfbabc8
Create Date: 2026-06-29 04:22:39.443896

"""
import uuid
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'f449f824bb08'
down_revision: str | None = 'a8913cfbabc8'
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


OWASP_CHEATSHEETS = [
    (
        "A01:2021",
        "Broken Access Control",
        """# A01:2021 - Broken Access Control

## Checklist
- Probar acceso directo a objetos por ID (IDOR): incrementar/decrementar IDs en URLs y JSON.
- Forzar navegación a endpoints de admin sin el rol adecuado.
- Verificar CORS mal configurado (`Access-Control-Allow-Origin: *` con credenciales).
- Probar escalado vertical (usuario normal accediendo a funciones de admin) y horizontal (usuario A accediendo a datos de usuario B).
- Revisar que el control de acceso se valide en el backend, no solo ocultando UI en el frontend.
- Probar manipulación de parámetros (`role=user` -> `role=admin`) en cookies/JWT/body.

## Payloads / pruebas rápidas
```
GET /api/users/1/profile      (autenticado como usuario 2)
PATCH /api/orders/123 {"user_id": 999}
GET /admin/dashboard           (sin rol admin)
```

## Mitigación
- Deny by default, validar autorización en cada request del lado servidor.
- Usar IDs no predecibles (UUID) y verificar ownership en cada consulta.
""",
    ),
    (
        "A02:2021",
        "Cryptographic Failures",
        """# A02:2021 - Cryptographic Failures

## Checklist
- Verificar que datos sensibles (passwords, tokens, PII) no se transmitan en texto plano (HTTP sin TLS).
- Revisar algoritmos de hash débiles (MD5, SHA1 sin salt) para passwords.
- Buscar claves/secrets hardcodeados en el código fuente o respuestas de la API.
- Verificar uso correcto de TLS (certificados válidos, sin downgrade a versiones inseguras).
- Revisar si se cachean o loguean datos sensibles innecesariamente.

## Herramientas
- `testssl.sh`, `sslyze` para configuración TLS.
- `nuclei -tags ssl,exposure` para secretos expuestos.

## Mitigación
- TLS 1.2+ en todo tránsito, bcrypt/argon2 para passwords.
- Cifrado en reposo para datos sensibles, gestión de secrets con vault dedicado.
""",
    ),
    (
        "A03:2021",
        "Injection",
        """# A03:2021 - Injection

## Checklist
- SQL Injection: probar comillas, comentarios SQL, `OR 1=1`, time-based blind.
- Command Injection: probar metacaracteres de shell en inputs que invocan procesos.
- NoSQL Injection: probar operadores Mongo (`$ne`, `$gt`) en JSON.
- Template Injection (SSTI): probar `{{7*7}}`, `${7*7}` según motor de plantillas.

## Payloads
```
' OR '1'='1
'; DROP TABLE users; --
1' AND SLEEP(5)--
| whoami
; id
{{7*7}}
${7*7}
```

## Herramientas
- `sqlmap -u <url> --batch --risk=2 --level=3`
- `nuclei -tags injection,sqli,rce`

## Mitigación
- Prepared statements / queries parametrizadas siempre.
- Validación estricta de input, listas blancas, escape de output contextual.
""",
    ),
    (
        "A04:2021",
        "Insecure Design",
        """# A04:2021 - Insecure Design

## Checklist
- Identificar flujos de negocio sin límites de rate (ej. reintentos infinitos de login, reset de password).
- Revisar lógica de negocio explotable (ej. carritos de compra con precios negativos, race conditions en transferencias).
- Verificar que existan controles anti-automatización (CAPTCHA, rate limiting) en funciones críticas.
- Buscar ausencia de modelado de amenazas en features sensibles (pagos, autenticación, recuperación de cuenta).

## Pruebas
- Repetir requests rápidamente para detectar race conditions (ej. doble canje de cupón).
- Probar flujos de negocio fuera del orden esperado (saltar pasos de un wizard).

## Mitigación
- Threat modeling en diseño, límites de negocio aplicados server-side, rate limiting por usuario/IP.
""",
    ),
    (
        "A05:2021",
        "Security Misconfiguration",
        """# A05:2021 - Security Misconfiguration

## Checklist
- Buscar paneles de administración expuestos, debug mode habilitado en producción.
- Revisar headers de seguridad faltantes (`CSP`, `X-Frame-Options`, `Strict-Transport-Security`).
- Verificar versiones de software/frameworks desactualizadas con vulnerabilidades conocidas.
- Buscar directory listing habilitado, archivos de backup/config expuestos (`.env`, `.git`, `web.config`).
- Revisar mensajes de error verbosos que filtran stack traces o rutas internas.

## Herramientas
- `nuclei -tags misconfig,exposure,tech`
- `whatweb`, `httpx -title -status-code -tech-detect`

## Mitigación
- Hardening de servidores/frameworks, deshabilitar features no usadas, gestión de configuración como código revisada.
""",
    ),
    (
        "A06:2021",
        "Vulnerable and Outdated Components",
        """# A06:2021 - Vulnerable and Outdated Components

## Checklist
- Fingerprinting de tecnologías (frameworks, librerías JS, CMS, versiones de servidor).
- Cruzar versiones detectadas contra CVEs conocidos.
- Revisar dependencias de terceros sin mantenimiento o con vulnerabilidades públicas.

## Herramientas
- `whatweb`, `httpx -tech-detect`
- `nuclei -tags cve` contra fingerprints detectados
- `nmap -sV --script vuln`

## Mitigación
- Inventario de componentes (SBOM), actualizaciones regulares, monitoreo de CVEs para el stack usado.
""",
    ),
    (
        "A07:2021",
        "Identification and Authentication Failures",
        """# A07:2021 - Identification and Authentication Failures

## Checklist
- Probar fuerza bruta / credential stuffing sin bloqueo de cuenta.
- Verificar políticas débiles de password (sin longitud mínima, sin verificación de breach).
- Revisar gestión de sesión: tokens predecibles, no invalidados tras logout, sin expiración.
- Probar bypass de MFA (reutilización de código, ausencia de rate limit en OTP).
- Revisar flujo de "recuperar contraseña" por tokens predecibles o sin expiración.

## Payloads / pruebas
```
POST /login  (mismo usuario, miles de intentos de password)
GET /reset-password?token=000001 ... 000999
```

## Mitigación
- MFA, rate limiting + lockout progresivo, tokens de sesión aleatorios con expiración, invalidación server-side en logout.
""",
    ),
    (
        "A08:2021",
        "Software and Data Integrity Failures",
        """# A08:2021 - Software and Data Integrity Failures

## Checklist
- Revisar actualizaciones de software sin verificación de firma/integridad.
- Buscar deserialización insegura de datos no confiables (pickle, Java serialization, PHP unserialize).
- Verificar pipelines CI/CD sin protección de integridad (dependencias no fijadas, sin lockfiles).
- Revisar uso de CDNs/scripts de terceros sin Subresource Integrity (SRI).

## Pruebas
- Probar payloads de deserialización conocidos (`ysoserial` para Java, gadgets de pickle en Python).
- Revisar `package-lock.json`/`requirements.txt` por dependencias sin pinning.

## Mitigación
- Firmas digitales en actualizaciones, evitar deserialización de datos no confiables, SRI en recursos externos.
""",
    ),
    (
        "A09:2021",
        "Security Logging and Monitoring Failures",
        """# A09:2021 - Security Logging and Monitoring Failures

## Checklist
- Verificar si eventos críticos (logins fallidos, cambios de permisos, accesos a datos sensibles) se registran.
- Revisar si los logs incluyen suficiente contexto (usuario, IP, timestamp) sin exponer datos sensibles.
- Probar si ataques evidentes (fuerza bruta, scanning) generan alertas o quedan invisibles.
- Verificar protección de logs contra tampering (acceso restringido, almacenamiento centralizado).

## Pruebas
- Generar actividad anómala (múltiples 401/403, payloads de inyección) y verificar si se detecta/alerta.

## Mitigación
- Logging centralizado, alertas en tiempo real para eventos de seguridad, retención adecuada y protección de integridad de logs.
""",
    ),
    (
        "A10:2021",
        "Server-Side Request Forgery (SSRF)",
        """# A10:2021 - Server-Side Request Forgery (SSRF)

## Checklist
- Identificar funcionalidades que hacen requests a URLs proporcionadas por el usuario (webhooks, importar imagen/PDF desde URL, previews de links).
- Probar acceso a metadata de cloud (`169.254.169.254`) y servicios internos (`localhost`, rangos privados).
- Probar bypass de filtros de URL: redirecciones, DNS rebinding, IPs en notación alternativa (decimal, hex, IPv6).

## Payloads
```
http://169.254.169.254/latest/meta-data/
http://localhost:6379/
http://127.0.0.1:80/admin
http://0177.0.0.1/   (notación octal de 127.0.0.1)
```

## Herramientas
- `nuclei -tags ssrf`

## Mitigación
- Listas blancas estrictas de destinos permitidos, deshabilitar redirects automáticos, segmentación de red para servicios internos.
""",
    ),
]


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('knowledge_documents',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('doc_type', sa.Enum('markdown', 'pdf', name='knowledge_document_type'), nullable=False),
    sa.Column('status', sa.Enum('ready', 'processing', 'failed', name='knowledge_document_status'), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('file_path', sa.String(length=512), nullable=True),
    sa.Column('owasp_categories', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('is_seed', sa.Boolean(), nullable=False),
    sa.Column('error_message', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('findings',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('engagement_id', sa.UUID(), nullable=False),
    sa.Column('source_job_id', sa.UUID(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('owasp_category', sa.String(length=16), nullable=False),
    sa.Column('severity', sa.Enum('critical', 'high', 'medium', 'low', 'info', name='finding_severity'), nullable=False),
    sa.Column('cvss_score', sa.Float(), nullable=True),
    sa.Column('status', sa.Enum('open', 'confirmed', 'fixed', 'false_positive', name='finding_status'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['engagement_id'], ['engagements.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['source_job_id'], ['jobs.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

    op.execute(
        """
        ALTER TABLE knowledge_documents
        ADD COLUMN search_vector tsvector
        GENERATED ALWAYS AS (
            setweight(to_tsvector('spanish', coalesce(title, '')), 'A') ||
            setweight(to_tsvector('spanish', coalesce(content, '')), 'B')
        ) STORED
        """
    )
    op.execute(
        "CREATE INDEX ix_knowledge_documents_search_vector "
        "ON knowledge_documents USING GIN (search_vector)"
    )

    now = sa.text("now()")
    rows = [
        {
            "id": uuid.uuid5(uuid.NAMESPACE_URL, f"cyberswiss-owasp-seed-{code}"),
            "title": f"{code} - {name}",
            "doc_type": "markdown",
            "status": "ready",
            "content": content,
            "file_path": None,
            "owasp_categories": [code],
            "is_seed": True,
            "error_message": None,
        }
        for code, name, content in OWASP_CHEATSHEETS
    ]
    knowledge_documents = sa.table(
        "knowledge_documents",
        sa.column("id", sa.UUID()),
        sa.column("title", sa.String()),
        sa.column("doc_type", sa.Enum("markdown", "pdf", name="knowledge_document_type")),
        sa.column("status", sa.Enum("ready", "processing", "failed", name="knowledge_document_status")),
        sa.column("content", sa.Text()),
        sa.column("file_path", sa.String()),
        sa.column("owasp_categories", postgresql.JSONB()),
        sa.column("is_seed", sa.Boolean()),
        sa.column("error_message", sa.Text()),
    )
    op.bulk_insert(knowledge_documents, rows)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('findings')
    op.drop_index('ix_knowledge_documents_search_vector', table_name='knowledge_documents')
    op.drop_table('knowledge_documents')
    # ### end Alembic commands ###
