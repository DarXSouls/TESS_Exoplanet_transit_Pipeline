"""
==========================================================
Representation Generation Layer (RGL)

Quality flag cleaner.

Removes cadences whose QUALITY flag indicates unreliable
photometric measurements.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

import pandas as pd

from preprocessing.cleaners.cleaner_base import (
    CleanerPlugin,
)
from preprocessing.config import PreprocessingConfig
from preprocessing.constants import (
    QUALITY_COLUMN,
)
from preprocessing.identifiers import CleanerID

from collections.abc import Mapping
from typing import Any




class QualityCleaner(CleanerPlugin):
    """
    Removes rows with non-zero QUALITY flags.
    """

    @property
    def id(self) -> CleanerID:
        return CleanerID.QUALITY

    @property
    def name(self) -> str:
        return "Quality Cleaner"

    @property
    def description(self) -> str:
        return (
            "Removes cadences with non-zero QUALITY flags."
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
        Remove cadences with non-zero QUALITY flags.
        """

        #
        # Nothing to do if QUALITY is absent.
        #
        if QUALITY_COLUMN not in dataframe.columns:
            return dataframe.copy()

        cleaned = dataframe.loc[
            dataframe[QUALITY_COLUMN] == 0
        ].copy()

        cleaned.reset_index(
            drop=True,
            inplace=True,
        )

        return cleaned

# TODO (V3):
# Support configurable QUALITY masks.