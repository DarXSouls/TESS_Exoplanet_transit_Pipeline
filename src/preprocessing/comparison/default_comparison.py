"""
==========================================================
Representation Generation Layer (RGL)

Default comparison plugin.

Selects the best representation from a collection of
evaluated representations.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from preprocessing.comparison.comparison_base import (
    ComparisonPlugin,
)
from preprocessing.config import PreprocessingConfig
from preprocessing.identifiers import ComparisonID
from preprocessing.preprocessing_models.metrics_models import (
    RepresentationComparison,
    RepresentationMetrics,
)


 
# Default Comparison

class DefaultComparison(ComparisonPlugin):
    """
    Default comparison strategy.

    When only a single representation is available,
    it is automatically selected as the best
    representation.
    """

    @property
    def id(self) -> ComparisonID:
        return ComparisonID.DEFAULT

    @property
    def name(self) -> str:
        return "Default Comparison"

    @property
    def description(self) -> str:
        return (
            "Baseline comparison strategy."
        )

    @property
    def version(self) -> tuple[int, int, int]:
        return (1, 0, 0)

    @property
    def enabled(self) -> bool:
        return True

    @property
    def default_config(
        self,
    ) -> Mapping[str, Any]:
        return {}

    def compare(
        self,
        metrics: Mapping[
            str,
            RepresentationMetrics,
        ],
        config: PreprocessingConfig,
    ) -> RepresentationComparison:
        """
        Compare representations.

        The default implementation assumes a single
        representation and selects it automatically.
        """

        if not metrics:
            raise ValueError(
                "No representation metrics supplied."
            )

        representation_scores = {
            representation_id: (
                metric.quality_score
                if metric.quality_score is not None
                else 0.0
            )
            for representation_id, metric in metrics.items()
        }

        best_representation = max(
            representation_scores,
            key=representation_scores.get,
        )

        ranking = tuple(
            sorted(
                representation_scores,
                key=representation_scores.get,
                reverse=True,
            )
        )

        return RepresentationComparison(
            representation_scores=representation_scores,
            best_representation=best_representation,
            ranking=ranking,
            comparison_method="default",
            comparison_version=(1, 0, 0),
        )