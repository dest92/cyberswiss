import asyncio
from dataclasses import dataclass

import docker
import redis as redis_sync

from app.core.config import settings

EOF_MARKER = "__CYBERSWISS_EOF__"


class DockerToolTimeoutError(Exception):
    pass


@dataclass
class ContainerRunResult:
    stdout: str
    exit_code: int
    container_id: str


def _run_container_sync(
    image: str,
    command: list[str],
    stdin_data: bytes | None,
    timeout: int,
    mem_limit: str,
    cpu_limit: float,
    log_channel: str | None,
) -> ContainerRunResult:
    client = docker.from_env()
    redis_client = redis_sync.from_url(settings.redis_url) if log_channel else None

    container = client.containers.run(
        image,
        command,
        detach=True,
        stdin_open=stdin_data is not None,
        read_only=True,
        tmpfs={"/tmp": "size=64m"},
        mem_limit=mem_limit,
        nano_cpus=int(cpu_limit * 1_000_000_000),
        pids_limit=256,
        security_opt=["no-new-privileges"],
        cap_drop=["ALL"],
        network_mode="bridge",
    )
    try:
        if stdin_data is not None:
            sock = container.attach_socket(params={"stdin": 1, "stream": 1})
            sock._sock.sendall(stdin_data)
            sock.close()

        chunks: list[str] = []
        for chunk in container.logs(stream=True, follow=True):
            text = chunk.decode("utf-8", errors="replace")
            chunks.append(text)
            if redis_client is not None:
                redis_client.publish(log_channel, text)

        try:
            wait_result = container.wait(timeout=timeout)
        except Exception as exc:
            try:
                container.kill()
            except docker.errors.APIError:
                pass
            raise DockerToolTimeoutError(
                f"La herramienta excedió el timeout de {timeout}s"
            ) from exc

        return ContainerRunResult(
            stdout="".join(chunks),
            exit_code=wait_result.get("StatusCode", -1),
            container_id=container.id,
        )
    finally:
        if redis_client is not None:
            redis_client.publish(log_channel, EOF_MARKER)
            redis_client.close()
        try:
            container.remove(force=True)
        except docker.errors.NotFound:
            pass


async def run_tool_container(
    image: str,
    command: list[str],
    *,
    stdin_data: bytes | None = None,
    timeout: int | None = None,
    mem_limit: str | None = None,
    cpu_limit: float | None = None,
    log_channel: str | None = None,
) -> ContainerRunResult:
    return await asyncio.to_thread(
        _run_container_sync,
        image,
        command,
        stdin_data,
        timeout or settings.job_default_timeout_seconds,
        mem_limit or settings.job_default_memory_limit,
        cpu_limit or settings.job_default_cpu_limit,
        log_channel,
    )
