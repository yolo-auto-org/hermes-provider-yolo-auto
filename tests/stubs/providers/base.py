"""Stand-in for ``providers.base.ProviderProfile``.

A dataclass mirroring the current Hermes field set (core ``providers/base.py``,
main branch, September 2026). The plugin filters its declared fields through
``dataclasses.fields``, so the stub doubles as the contract test for field
drift: removing ``model_capabilities`` from this dataclass makes the plugin's
introspection drop it, exactly as it would on an older Hermes build.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class ProviderProfile:
    name: str = ""
    api_mode: str = "chat_completions"
    aliases: tuple = ()
    display_name: str = ""
    description: str = ""
    signup_url: str = ""
    env_vars: tuple = ()
    base_url: str = ""
    models_url: str = ""
    auth_type: str = "api_key"
    supports_health_check: bool = True
    supports_model_listing: bool = True
    auth_handler: Optional[Callable] = None
    refresh_credential: Optional[Callable] = None
    classify_api_error: Optional[Callable] = None
    supports_vision: bool = False
    supports_vision_tool_messages: bool = True
    supports_prompt_cache_key: bool = False
    native_reasoning_details_type: Optional[str] = None
    process_command: str = ""
    process_args: tuple = ()
    fallback_models: tuple = ()
    model_aliases: dict = field(default_factory=dict)
    hostname: str = ""
    default_headers: dict = field(default_factory=dict)
    fixed_temperature: Any = None
    default_max_tokens: Optional[int] = None
    unsupported_response_formats: tuple = ()
    default_aux_model: str = ""
    model_capabilities: dict = field(default_factory=dict)

    def fetch_models(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 8.0,
    ) -> Optional[list]:
        """Record the call; real core hits {models_url or base_url}/models."""
        return None
