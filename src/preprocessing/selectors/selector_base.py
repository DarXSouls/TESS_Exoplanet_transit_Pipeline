"""
==========================================================
Representation Generation Layer (RGL)

Base selector interface used by the preprocessing
framework.

Every flux selector plugin inherits from this class.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from abc import abstractmethod

from preprocessing.config import PreprocessingConfig
from preprocessing.identifiers import SelectorID
from preprocessing.plugins.base_plugin import BasePlugin
from preprocessing.preprocessing_models.input_models import (
    FluxSelectionResult,
    PreprocessInput
)

import pandas as pd


 
# Selector Plugin

class SelectorPlugin(BasePlugin):
    """
    Abstract base class for all flux selector plugins.

    A selector is responsible for choosing the most
    appropriate flux representation from the raw input
    data and returning the selection result.
    """

    @property
    @abstractmethod
    def id(self) -> SelectorID:
        """
        Unique selector identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def select(
        self,
        raw_dataframe: pd.DataFrame,
        input_data: PreprocessInput,
        config: PreprocessingConfig
    ) -> FluxSelectionResult:
        """
        Select the flux representation to be used by the
        preprocessing pipeline.

        Parameters
        ----------
        input_data
            Input data for one target.

        config
            Framework preprocessing configuration.

        Returns
        -------
        FluxSelectionResult
            Result of the flux selection stage.
        """
        raise NotImplementedError