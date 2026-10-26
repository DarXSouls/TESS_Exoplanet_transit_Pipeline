"""
==========================================================
Representation Generation Layer (RGL)

Registry for flux selector plugins.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from preprocessing.identifiers import SelectorID
from preprocessing.registry.base_registry import BaseRegistry
from preprocessing.selectors.selector_base import (
    SelectorPlugin,
)


 
# Selector Registry

class SelectorRegistry(
    BaseRegistry[
        SelectorID,
        SelectorPlugin,
    ]
):
    """
    Registry for flux selector plugins.
    """

    def register(
        self,
        plugin: SelectorPlugin,
    ) -> SelectorPlugin:
        """
        Register a selector plugin.
        """

        return super().register(
            plugin.id,
            plugin,
        )
