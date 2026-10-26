"""
==========================================================
Representation Generation Layer (RGL)

Missing value cleaner.

Removes cadences containing missing values in the
essential photometric columns.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pandas as pd

from preprocessing.cleaners.cleaner_base import (
    CleanerPlugin,
)
from preprocessing.config import PreprocessingConfig
from preprocessing.constants import (
    ESSENTIAL_LIGHTCURVE_COLUMNS,
    TIMESTAMP_COLUMNS,
)
from preprocessing.identifiers import CleanerID

import numpy as np



class MissingValueCleaner(CleanerPlugin):
    """
    Cleans the light curve by:

    - replacing infinite values with NaN
    - removing missing essential photometric values
    - removing duplicate timestamps
    - resetting the dataframe index
    """

    @property
    def id(self) -> CleanerID:
        return CleanerID.MISSING_VALUES

    @property
    def name(self) -> str:
        return "Missing Value Cleaner"

    @property
    def description(self) -> str:
        return (
            "Removes rows containing missing values."
        )

    @property
    def version(self) -> tuple[int, int, int]:
        return (1, 0, 0)

    @property
    def enabled(self) -> bool:
        return True

    @property
    def default_config(self) -> Mapping[str, Any]:
        return {}

    def clean(
        self,
        dataframe: pd.DataFrame,
        config: PreprocessingConfig,
    ) -> pd.DataFrame:
        """
        Remove rows containing missing values.
        """

        #
        # TODO (V3)
        #
        # Allow configurable subsets of required columns.
        #

        cleaned = dataframe.copy()

        cleaned[
            ESSENTIAL_LIGHTCURVE_COLUMNS
        ] = cleaned[
            ESSENTIAL_LIGHTCURVE_COLUMNS
        ].replace(
            [np.inf, -np.inf],
            np.nan,
        )

        cleaned = cleaned.dropna(
            subset=ESSENTIAL_LIGHTCURVE_COLUMNS
        )

        cleaned = cleaned.drop_duplicates(
            subset=TIMESTAMP_COLUMNS
        )

        cleaned.reset_index(
            drop=True,
            inplace=True,
        )

        if cleaned.empty:
            raise ValueError(
                "No valid cadences remain after cleaning."
            )

        return cleaned