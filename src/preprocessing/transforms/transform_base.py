"""
==========================================================
Representation Generation Layer (RGL)

Base transform interface used by the preprocessing
framework.

Every preprocessing transform plugin inherits from
this class.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from abc import abstractmethod

from preprocessing.config import PreprocessingConfig
from preprocessing.identifiers import TransformID
from preprocessing.plugins.base_plugin import BasePlugin
from preprocessing.preprocessing_models.input_models import (
    FluxSelectionResult,
)
from preprocessing.preprocessing_models.representation_models import (
    Representation,
)

import pandas as pd

 
# Transform Plugin

class TransformPlugin(BasePlugin):
    """
    Abstract base class for preprocessing transform plugins.

    A transform receives the selected flux representation
    and generates one scientific representation.
    """

    @property
    @abstractmethod
    def id(self) -> TransformID:
        """
        Unique transform identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def transform(
        self,
        cleaned_dataframe: pd.DataFrame,
        flux_selection: FluxSelectionResult,
        config: PreprocessingConfig
    ) -> Representation:
        """
        Generate a scientific representation.

        Parameters
        ----------
        flux_selection
            Result produced by the selector.

        config
            Framework preprocessing configuration.

        Returns
        -------
        Representation
            Generated scientific representation.
        """
        raise NotImplementedError