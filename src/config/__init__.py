from src.config.settings import Settings, get_settings

__all__ = ["Settings", "get_settings", "settings"]


def __getattr__(name: str):
    if name == "settings":
        return get_settings()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
