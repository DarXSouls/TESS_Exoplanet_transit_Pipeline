"""
==========================================================
Representation Generation Layer (RGL)

Registry for Comparison strategy plugins.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from preprocessing.identifiers import ComparisonID
from preprocessing.registry.base_registry import BaseRegistry
from preprocessing.comparison.comparison_base import ComparisonPlugin


 
# Comparison Registry

class ComparisonRegistry(
    BaseRegistry[
        ComparisonID,
        ComparisonPlugin,
    ]
):

    def register(
        self,
        plugin: ComparisonPlugin,
    ) -> ComparisonPlugin:

        return super().register(
            plugin.id,
            plugin,
        )