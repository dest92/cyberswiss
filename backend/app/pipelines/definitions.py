from typing import Any

from app.pipelines.base import PipelineDefinition, PipelineStep
from app.tools.base import NormalizedResult, ResultType


def _values_of(results: list[NormalizedResult], result_type: ResultType) -> list[str]:
    return [r.value for r in results if r.type == result_type]


RECON_CHAIN = PipelineDefinition(
    name="recon_chain",
    steps=[
        PipelineStep(
            tool_name="subfinder",
            build_params=lambda params, prev: {"domain": params["domain"]},
        ),
        PipelineStep(
            tool_name="httpx",
            build_params=lambda params, prev: {
                "targets": _values_of(prev, ResultType.host) or [params["domain"]]
            },
        ),
        PipelineStep(
            tool_name="nuclei",
            build_params=lambda params, prev: {"targets": _values_of(prev, ResultType.url)},
        ),
    ],
)


def _gobuster_targets(params: dict[str, Any], prev: list[NormalizedResult]) -> list[str]:
    base_url = params["url"].rstrip("/")
    paths = _values_of(prev, ResultType.url)
    return [base_url] + [f"{base_url}{path}" for path in paths]


WEB_AUDIT = PipelineDefinition(
    name="web_audit",
    steps=[
        PipelineStep(
            tool_name="httpx",
            build_params=lambda params, prev: {"targets": [params["url"]]},
        ),
        PipelineStep(
            tool_name="whatweb",
            build_params=lambda params, prev: {"url": params["url"]},
        ),
        PipelineStep(
            tool_name="gobuster",
            build_params=lambda params, prev: {"url": params["url"]},
        ),
        PipelineStep(
            tool_name="nuclei",
            build_params=lambda params, prev: {"targets": _gobuster_targets(params, prev)},
        ),
    ],
)

PIPELINES: dict[str, PipelineDefinition] = {
    RECON_CHAIN.name: RECON_CHAIN,
    WEB_AUDIT.name: WEB_AUDIT,
}


def get_pipeline(name: str) -> PipelineDefinition:
    try:
        return PIPELINES[name]
    except KeyError:
        raise ValueError(f"Pipeline desconocido: {name}") from None


def list_pipelines() -> list[str]:
    return sorted(PIPELINES)
