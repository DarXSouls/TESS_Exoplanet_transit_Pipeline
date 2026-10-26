"""
==========================================================
Representation Generation Layer (RGL)

Registry for representation Metric plugins.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from preprocessing.identifiers import MetricID
from preprocessing.registry.base_registry import BaseRegistry
from preprocessing.metrics.metric_base import MetricPlugin


 
# Metrics Registry

class MetricRegistry(
    BaseRegistry[
        MetricID,
        MetricPlugin,
    ]
):

    def register(
        self,
        plugin: MetricPlugin,
    ) -> MetricPlugin:

        return super().register(
            plugin.id,
            plugin,
        )