"""
==========================================================
Representation Generation Layer (RGL)

Global median normalization transform.

Normalizes the selected flux by dividing the flux and its
uncertainty by the global median.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from collections import OrderedDict
from collections.abc import Mapping
from typing import Any

import numpy as np
import pandas as pd

from preprocessing.config import PreprocessingConfig
from preprocessing.identifiers import TransformID
from preprocessing.enums import (
    RepresentationStatus,
    RepresentationType,
    TransformCategory,
)
from preprocessing.preprocessing_models.input_models import (
    FluxSelectionResult,
)
from preprocessing.preprocessing_models.representation_models import (
    Representation,
    RepresentationColumns,
    TransformStep,
)
from preprocessing.transforms.transform_base import (
    TransformPlugin,
)


 
# Global Median Transform

class GlobalMedianTransform(TransformPlugin):
    """
    Normalize the selected flux using its global median.
    """

    @property
    def id(self) -> TransformID:
        return TransformID.GLOBAL_MEDIAN

    @property
    def name(self) -> str:
        return "Global Median"

    @property
    def description(self) -> str:
        return (
            "Normalizes the selected flux using the "
            "global median."
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

    def transform(
        self,
        cleaned_dataframe: pd.DataFrame,
        flux_selection: FluxSelectionResult,
        config: PreprocessingConfig,
    ) -> Representation:
        """
        Generate a globally median-normalized
        representation.
        """

        flux = flux_selection.selected_flux.flux.copy()
        flux_error = flux_selection.selected_flux.flux_error.copy()

        median = float(np.nanmedian(flux))

        if median == 0.0:
            raise ValueError(
                "Cannot normalize using a zero median."
            )

        normalized_flux = flux / median
        normalized_error = flux_error / median

        columns = RepresentationColumns(
            columns=OrderedDict(
                {
                    "NORMALIZED_FLUX": normalized_flux,
                    "NORMALIZED_FLUX_ERR": normalized_error,
                }
            )
        )

        transform_step = TransformStep(
            plugin_name=self.name,
            plugin_version=self.version,
            plugin_category=TransformCategory.NORMALIZATION,
            transform_parameters={},
            input_columns=(
                "FLUX",
                "FLUX_ERR",
            ),
            output_columns=(
                "NORMALIZED_FLUX",
                "NORMALIZED_FLUX_ERR",
            ),
            execution_order=1,
            execution_time_seconds=None,
        )

        return Representation(
            representation_id="GLOBAL_MEDIAN",
            display_name="Global Median",
            representation_type=RepresentationType.BASELINE,
            status=RepresentationStatus.CREATED,
            source_flux=flux_selection.selected_flux_type,
            transform_steps=(transform_step,),
            columns=columns,
        )