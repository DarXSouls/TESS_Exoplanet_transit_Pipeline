"""
==========================================================
Representation Generation Layer (RGL)

Input models used by the preprocessing framework.

These dataclasses describe the information entering the
Representation Generation Layer.

Author : Shyam Girish Chinta
==========================================================
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from collections.abc import Mapping

import pandas as pd

from preprocessing.enums import (
    FluxSelectionMethod,
    FluxType
)


  
# Preprocess Input

@dataclass(
    slots=True,
    frozen=True
)
class PreprocessInput:
    """
    Input required to preprocess a single target.
    """

    tic_id: int

    label: str

    catalog: str

    parquet_file: Path

    @property
    def target_directory(self) -> str:
        return f"TIC_{self.tic_id}"





@dataclass(
    slots=True,
    frozen=True
)
class FluxData:

    """
    Flux values together with their
    associated uncertainties.
    """

    flux: pd.Series

    flux_error: pd.Series

    flux_column: str

    flux_error_column: str



  
# Flux Selection Result

@dataclass(
    slots=True,
    frozen=True
)
class FluxSelectionResult:
    """
    Result produced by a flux selector.

    This object records which flux was selected together
    with the selection scores and supporting metadata.
    """

    selected_flux_type: FluxType

    selected_flux: FluxData

    selection_method: FluxSelectionMethod

    selection_scores: Mapping[
        FluxType,
        float
    ] = field(
        default_factory=dict
    )

    metadata: Mapping[
        str,
        Any
    ] = field(
        default_factory=dict
    )

    # TODO:
    # Preserve SmartSelector quality metrics
    # in FluxSelectionResult once selector
    # diagnostics are supported.