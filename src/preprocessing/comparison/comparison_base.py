"""
==========================================================
Representation Generation Layer (RGL)

Base comparison interface used by the preprocessing
framework.

Every comparison strategy inherits from this class.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from abc import abstractmethod

from collections.abc import Mapping

from preprocessing.config import PreprocessingConfig
from preprocessing.identifiers import ComparisonID
from preprocessing.plugins.base_plugin import BasePlugin
from preprocessing.preprocessing_models.metrics_models import (
    RepresentationComparison,
    RepresentationMetrics,
)


 
# Comparison Plugin

class ComparisonPlugin(BasePlugin):
    """
    Abstract base class for representation comparison
    plugins.

    A comparison plugin evaluates multiple
    representations and selects the best one.
    """

    @property
    @abstractmethod
    def id(self) -> ComparisonID:
        """
        Unique comparison identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def compare(
        self,
        metrics: Mapping[
            str,
            RepresentationMetrics,
        ],
        config: PreprocessingConfig
    ) -> RepresentationComparison:
        """
        Compare multiple scientific representations.

        Parameters
        ----------
        metrics
            Evaluation metrics for all generated
            representations.

        config
            Framework preprocessing configuration.

        Returns
        -------
        RepresentationComparison
            Comparison results and selected best
            representation.
        """
        raise NotImplementedError