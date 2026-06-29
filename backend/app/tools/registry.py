from app.tools.base import ToolAdapter

_REGISTRY: dict[str, ToolAdapter] = {}


def register(adapter: ToolAdapter) -> None:
    _REGISTRY[adapter.name] = adapter


def get_adapter(name: str) -> ToolAdapter:
    try:
        return _REGISTRY[name]
    except KeyError:
        raise ValueError(f"Herramienta desconocida: {name}") from None


def list_tools() -> list[str]:
    return sorted(_REGISTRY)
