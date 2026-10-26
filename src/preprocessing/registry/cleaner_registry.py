"""
==========================================================
Representation Generation Layer (RGL)

Registry for dataframe cleaning plugins.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from preprocessing.cleaners.cleaner_base import CleanerPlugin
from preprocessing.identifiers import CleanerID
from preprocessing.registry.base_registry import BaseRegistry


class CleanerRegistry(
    BaseRegistry[
        CleanerID,
        CleanerPlugin,
    ]
):
    """
    Registry for dataframe cleaning plugins.
    """

    def register(
        self,
        plugin: CleanerPlugin,
    ) -> CleanerPlugin:

        return super().register(
            plugin.id,
            plugin,
        )