"""
==========================================================
Representation Generation Layer (RGL)

Base interface for dataframe cleaning plugins.

Cleaning plugins prepare validated light curves before
flux selection and representation generation.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Mapping
from typing import Any

import pandas as pd

from preprocessing.config import PreprocessingConfig
from preprocessing.identifiers import (
    CleanerID
)




# Cleaner Plugin

class CleanerPlugin(ABC):
    """
    Base interface for dataframe cleaning plugins.

    Cleaning plugins receive a validated dataframe and
    return a cleaned dataframe.
    """

    @property
    @abstractmethod
    def id(self) -> CleanerID:
        """
        Unique cleaner identifier.
        """
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human-readable cleaner name.
        """
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Cleaner description.
        """
        ...

    @property
    @abstractmethod
    def version(
        self,
    ) -> tuple[int, int, int]:
        """
        Cleaner version.
        """
        ...

    @property
    @abstractmethod
    def enabled(self) -> bool:
        """
        Whether this cleaner is enabled.
        """
        ...

    @property
    @abstractmethod
    def default_config(
        self,
    ) -> Mapping[str, Any]:
        """
        Default cleaner configuration.
        """
        ...

    @abstractmethod
    def clean(
        self,
        dataframe: pd.DataFrame,
        config: PreprocessingConfig,
    ) -> pd.DataFrame:
        """
        Clean the dataframe.

        Parameters
        ----------
        dataframe
            Validated dataframe.

        config
            Global preprocessing configuration.

        Returns
        -------
        pd.DataFrame
            Cleaned dataframe.
        """
        ...