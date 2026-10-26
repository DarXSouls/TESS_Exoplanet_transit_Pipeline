"""
==========================================================
Representation Generation Layer (RGL)

Registry for preprocessing Transform plugins.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from preprocessing.identifiers import TransformID
from preprocessing.registry.base_registry import BaseRegistry
from preprocessing.transforms.transform_base import TransformPlugin


 
# Transform Registry

class TransformRegistry(
    BaseRegistry[
        TransformID,
        TransformPlugin,
    ]
):

    def register(
        self,
        plugin: TransformPlugin,
    ) -> TransformPlugin:

        return super().register(
            plugin.id,
            plugin,
        )