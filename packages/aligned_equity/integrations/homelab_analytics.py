from __future__ import annotations

"""Import-safe homelab-analytics registry hooks.

The initialization baseline deliberately registers no executable extensions or
publications. Future work can add contract-bearing registrations here without
making homelab-analytics a core package dependency.
"""


def register_extensions(registry: object) -> None:
    _ = registry


def register_pipeline_registries(**registries: object) -> None:
    _ = registries


def register_functions(registry: object) -> None:
    _ = registry


def register_capability_packs(registry: object) -> None:
    _ = registry
