"""
==========================================================
Representation Generation Layer (RGL)

Base metric interface used by the preprocessing
framework.

Every representation metric plugin inherits from
this class.

Author : Shyam Girish Chinta
Project: ISRO Exoplanet Detection Pipeline
==========================================================
"""

from __future__ import annotations

from abc import abstractmethod

from preprocessing.config import PreprocessingConfig
from preprocessing.identifiers import MetricID
from preprocessing.plugins.base_plugin import BasePlugin
from preprocessing.preprocessing_models.metrics_models import (
    RepresentationMetrics,
)
from preprocessing.preprocessing_models.representation_models import (
    Representation,
)

import pandas as pd

 
# Metric Plugin
 
class MetricPlugin(BasePlugin):
    """
    Abstract base class for representation metric plugins.

    A metric evaluates one scientific representation and
    produces quantitative evaluation metrics.
    """

    @property
    @abstractmethod
    def id(self) -> MetricID:
        """
        Unique metric identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def evaluate(
        self,
        cleaned_dataframe: pd.DataFrame,
        representation: Representation,
        config: PreprocessingConfig
    ) -> RepresentationMetrics:
        """
        Evaluate a scientific representation.

        Parameters
        ----------
        representation
            Scientific representation to evaluate.

        config
            Framework preprocessing configuration.

        Returns
        -------
        RepresentationMetrics
            Evaluation metrics for the representation.
        """
        raise NotImplementedError