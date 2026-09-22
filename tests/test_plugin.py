"""Unit tests for the yolo-auto Hermes model-provider plugin.

Run from the repository root:

    python -m unittest discover -s tests -p "test_*.py" -v

The tests import the plugin against the stub ``providers`` package in
``tests/stubs``, so they need neither a Hermes checkout nor network access.
They pin the contract the plugin relies on: registration shape, the
auto-discovery defaults (live ``GET {base_url}/models`` with Bearer auth), and
the field-introspection fallback for older Hermes builds.
"""

from __future__ import annotations

import dataclasses
import importlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests" / "stubs"))


def load_plugin():
    # The plugin registers at import time. Re-execute it against a fresh stub
    # registry on every load, or re-imports would skip registration.
    for module in ("providers", "providers.base", "yolo-auto"):
        sys.modules.pop(module, None)
    sys.path.insert(0, str(ROOT))
    try:
        return importlib.import_module("yolo-auto")
    finally:
        sys.path.remove(str(ROOT))

class RegistrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plugin = load_plugin()
        import providers

        self.profile = providers.REGISTRY.get("yolo-auto")

    def test_plugin_registers_the_provider(self) -> None:
        import providers

        self.assertIn("yolo-auto", providers.REGISTRY)
        self.assertIsNotNone(self.profile)

    def test_profile_wires_endpoint_and_auth(self) -> None:
        self.assertEqual(self.profile.base_url, "https://yolo-auto.com/v1")
        self.assertEqual(self.profile.auth_type, "api_key")
        self.assertEqual(self.profile.api_mode, "chat_completions")
        self.assertEqual(
            self.profile.env_vars, ("YOLO_AUTO_API_KEY", "YOLO_AUTO_BASE_URL")
        )
        self.assertEqual(self.profile.hostname, "yolo-auto.com")

    def test_auto_discovery_needs_no_curated_url(self) -> None:
        # Discovery is the inherited path: no models_url override, so Hermes
        # hits {base_url}/models with the Bearer key. The endpoint returns the
        # plan-filtered catalog, which is what keeps the picker honest.
        self.assertEqual(self.profile.models_url, "")

    def test_fallbacks_and_aux_model_are_flagship_model_ids(self) -> None:
        self.assertEqual(self.profile.default_aux_model, "yolo")
        self.assertEqual(self.profile.fallback_models, ("yolo", "yolo-small"))

    def test_every_fallback_declares_capabilities(self) -> None:
        # A fallback model the picker can show but capabilities cannot describe
        # falls through to the models.dev catalog, which does not know our ids.
        for model in self.profile.fallback_models:
            self.assertIn(model, self.profile.model_capabilities, model)

    def test_text_only_model_does_not_claim_vision(self) -> None:
        caps = self.profile.model_capabilities["yolo-small"]
        self.assertFalse(caps["supports_vision"])
        self.assertTrue(caps["supports_tools"])


class OlderBuildTests(unittest.TestCase):
    def test_unknown_fields_are_dropped_not_fatal(self) -> None:
        self.plugin = load_plugin()

        @dataclasses.dataclass
        class LegacyProfile:
            name: str = ""
            base_url: str = ""
            auth_type: str = "api_key"
            env_vars: tuple = ()

        kwargs = self.plugin._supported_kwargs(
            LegacyProfile,
            {
                "name": "yolo-auto",
                "base_url": "https://yolo-auto.com/v1",
                "model_capabilities": {"gone": {}},
                "supports_vision": True,
            },
        )
        self.assertEqual(
            kwargs,
            {
                "name": "yolo-auto",
                "base_url": "https://yolo-auto.com/v1",
            },
        )


if __name__ == "__main__":
    unittest.main()
