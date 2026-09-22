"""Minimal stand-in for Hermes' providers package.

Real Hermes discovers plugins by importing them and letting
``register_provider`` populate a process-global registry. The unit tests need
exactly that seam and nothing more, so the stub records registrations and the
tests assert against them. This keeps the plugin's tests runnable without a
Hermes checkout or network access.
"""

REGISTRY: dict[str, object] = {}


def register_provider(profile) -> None:  # noqa: ANN001 - mirrors Hermes signature
    REGISTRY[profile.name] = profile
