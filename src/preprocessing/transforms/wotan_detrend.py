"""
==========================================================
Representation Generation Layer (RGL)

Wotan detrending transform.

Applies Wotan detrending to a selected flux
representation while preserving the original
representation.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from collections import OrderedDict
from collections.abc import Mapping
from typing import Any

import numpy as np
import pandas as pd

from wotan import flatten

from preprocessing.config import (
    PreprocessingConfig,
)

from preprocessing.constants import (
    TIME_COLUMN,
    SECTOR_COLUMN,
    FLUX_ERROR_COLUMN,
    DETRENDED_FLUX_COLUMN,
    TREND_COLUMN,
    WOTAN_METHOD,
    WOTAN_WINDOW_LENGTH,
    WOTAN_BREAK_TOLERANCE,
    WOTAN_EDGE_CUTOFF,
)

from preprocessing.identifiers import (
    TransformID,
)

from preprocessing.preprocessing_models import (
    FluxSelectionResult,
    Representation,
    RepresentationColumns,
    TransformStep,
)

from preprocessing.enums import (
    RepresentationStatus,
    RepresentationType,
    TransformCategory,
)


from preprocessing.transforms.transform_base import (
    TransformPlugin,
)


class WotanDetrendTransform(
    TransformPlugin,
):
    """
    Apply Wotan detrending to the selected
    light-curve representation.
    """


    # Plugin Metadata

    @property
    def id(
        self,
    ) -> TransformID:

        return TransformID.WOTAN_DETREND

    @property
    def name(
        self,
    ) -> str:

        return "Wotan Detrending"

    @property
    def description(
        self,
    ) -> str:

        return (
            "Applies Wotan detrending to the "
            "selected flux representation."
        )

    @property
    def version(
        self,
    ) -> tuple[int, int, int]:

        return (1, 0, 0)

    @property
    def enabled(
        self,
    ) -> bool:

        return True

    @property
    def default_config(
        self,
    ) -> Mapping[str, Any]:

        return {

            "method": WOTAN_METHOD,

            "window_length": WOTAN_WINDOW_LENGTH,

            "break_tolerance": WOTAN_BREAK_TOLERANCE,

            "edge_cutoff": WOTAN_EDGE_CUTOFF,
        }

    
    # Validation

    def _validate(
        self,
        cleaned_dataframe: pd.DataFrame,
        flux_selection: FluxSelectionResult,
    ) -> None:
        """
        Validate the inputs required for
        Wotan detrending.
        """

        
        # Empty dataframe

        if cleaned_dataframe.empty:

            raise ValueError(
                "Cannot detrend an empty dataframe."
            )

        
        # Required columns

        required_columns = (
            TIME_COLUMN,
            SECTOR_COLUMN,
        )

        missing_columns = [
            column
            for column in required_columns
            if column not in cleaned_dataframe.columns
        ]

        if missing_columns:

            raise ValueError(
                "Missing required dataframe columns: "
                f"{missing_columns}"
            )

        
        # Flux length

        if (
            len(flux_selection.selected_flux.flux)
            != len(cleaned_dataframe)
        ):

            raise ValueError(
                "Selected flux length does not "
                "match dataframe."
            )

        
        # Flux error length

        if (
            len(
                flux_selection
                .selected_flux
                .flux_error
            )
            != len(cleaned_dataframe)
        ):

            raise ValueError(
                "Selected flux-error length does "
                "not match dataframe."
            )

    
    # Detrending Helpers

    def _detrend_sector(
        self,
        sector_dataframe: pd.DataFrame,
        flux_column: str,
        settings: Mapping[str, Any],
    ) -> pd.DataFrame:
        """
        Detrend a single observing sector using
        Wotan.
        """

        dataframe = sector_dataframe.copy()

        detrended_flux, trend = flatten(

            dataframe[TIME_COLUMN].to_numpy(),

            dataframe[flux_column].to_numpy(),

            method=settings["method"],

            window_length=settings["window_length"],

            break_tolerance=settings["break_tolerance"],

            edge_cutoff=settings["edge_cutoff"],

            return_trend=True,

        )

        dataframe[DETRENDED_FLUX_COLUMN] = detrended_flux

        dataframe[TREND_COLUMN] = trend

        if not np.isfinite(
            dataframe[DETRENDED_FLUX_COLUMN]
        ).all():

            raise ValueError(
                "Wotan produced invalid detrended flux."
            )

        if not np.isfinite(
            dataframe[TREND_COLUMN]
        ).all():

            raise ValueError(
                "Wotan produced invalid trend."
            )

        return dataframe

    def _detrend_dataframe(
        self,
        cleaned_dataframe: pd.DataFrame,
        flux_column: str,
    ) -> pd.DataFrame:
        """
        Detrend every observing sector
        independently.
        """

        settings = self.default_config

        detrended_sectors = []

        for _, sector_dataframe in (
            cleaned_dataframe.groupby(
                SECTOR_COLUMN
            )
        ):

            detrended_sectors.append(

                self._detrend_sector(

                    sector_dataframe,

                    flux_column,

                    settings,

                )

            )

        detrended_dataframe = pd.concat(

            detrended_sectors,

            ignore_index=True,

        )

        detrended_dataframe = (

            detrended_dataframe

            .sort_values(

                [SECTOR_COLUMN, TIME_COLUMN]

            )

            .reset_index(

                drop=True

            )

        )

        return detrended_dataframe

    def _build_representation(
        self,
        detrended_dataframe: pd.DataFrame,
        flux_selection: FluxSelectionResult,
    ) -> Representation:
        """
        Build the Wotan detrended representation.
        """


        # Representation Columns

        representation_columns = RepresentationColumns(

            columns=OrderedDict({

                DETRENDED_FLUX_COLUMN:
                    detrended_dataframe[
                        DETRENDED_FLUX_COLUMN
                    ],

                TREND_COLUMN:
                    detrended_dataframe[
                        TREND_COLUMN
                    ],

            })

        )

    
        # Transform Step

        transform_step = TransformStep(

            plugin_name=self.name,

            plugin_version=self.version,

            plugin_category=(
                TransformCategory.DETRENDING
            ),

            transform_parameters=dict(
                self.default_config
            ),

            input_columns=(
                flux_selection
                .selected_flux
                .flux_column,
            ),

            output_columns=(

                DETRENDED_FLUX_COLUMN,

                TREND_COLUMN,

            ),

            execution_order=1,

        )

    
        # Representation

        representation = Representation(

            representation_id=(
                TransformID.WOTAN_DETREND.value
            ),

            display_name=(
                "Wotan Detrended"
            ),

            representation_type=(
                RepresentationType.DETRENDED
            ),

            status=(
                RepresentationStatus.SUCCESS
            ),

            source_flux=(
                flux_selection
                .selected_flux_type
            ),

            transform_steps=(
                transform_step,
            ),

            columns=representation_columns,

            primary_flux_column=(
                DETRENDED_FLUX_COLUMN
            ),

            primary_flux_error_column=(
                FLUX_ERROR_COLUMN
            ),

        )

        return representation

    
    # Transform

    def transform(
        self,
        cleaned_dataframe: pd.DataFrame,
        flux_selection: FluxSelectionResult,
        config: PreprocessingConfig,
    ) -> Representation:

        self._validate(
            cleaned_dataframe,
            flux_selection,
        )

        detrended_dataframe = self._detrend_dataframe(

            cleaned_dataframe,

            flux_selection.selected_flux.flux_column,

        )

        return self._build_representation(

            detrended_dataframe,

            flux_selection,

        )