from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "cyberswiss"
    database_url: str = "postgresql+asyncpg://cyberswiss:cyberswiss@postgres/cyberswiss"
    redis_url: str = "redis://redis:6379/0"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 30
    auth_disabled: bool = False
    uploads_dir: str = "/app/data/uploads"
    job_outputs_dir: str = "/app/data/job_outputs"
    job_default_timeout_seconds: int = 600
    job_default_memory_limit: str = "512m"
    job_default_cpu_limit: float = 1.0
    recon_toolbox_image: str = "cyberswiss/recon-toolbox:latest"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]


settings = Settings()
