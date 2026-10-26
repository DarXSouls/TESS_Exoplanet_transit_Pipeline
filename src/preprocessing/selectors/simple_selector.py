"""
==========================================================
Representation Generation Layer (RGL)

Simple flux selector.

Selects the flux type with the largest number of valid
(non-missing) cadences.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from preprocessing.identifiers import SelectorID
from preprocessing.config import PreprocessingConfig

from preprocessing.enums import (
    FluxSelectionMethod,
    FluxType,
)

from preprocessing.preprocessing_models.input_models import (
    FluxData,
    FluxSelectionResult,
    PreprocessInput,
)

from preprocessing.selectors.selector_base import (
    SelectorPlugin,
)

import pandas as pd

from collections.abc import Mapping
from typing import Any

 
# Simple Selector

class SimpleSelector(SelectorPlugin):
    """
    Simple flux selector.

    Chooses the flux type containing the greatest number
    of valid cadences.
    """

    @property
    def id(self) -> SelectorID:
        return SelectorID.SIMPLE

    @property
    def name(self) -> str:
        return "Simple Selector"

    @property
    def description(self) -> str:
        return (
            "Selects the flux with the highest number "
            "of valid cadences."
        )

    @property
    def version(self) -> tuple[int, int, int]:
        return (1, 0, 0)

    @property
    def enabled(self) -> bool:
        return True

    @property
    def default_config(
        self,
    ) -> Mapping[str, Any]:
        return {}

    def select(
        self,
        raw_dataframe: pd.DataFrame,
        input_data: PreprocessInput,
        config: PreprocessingConfig,
    ) -> FluxSelectionResult:
        """
        Select the preferred flux representation.
        """

        pdcsap_score = float(
            raw_dataframe["PDCSAP_FLUX"].notna().sum()
        )

        sap_score = float(
            raw_dataframe["SAP_FLUX"].notna().sum()
        )

        scores = {
            FluxType.PDCSAP: pdcsap_score,
            FluxType.SAP: sap_score,
        }

        if pdcsap_score >= sap_score:

            flux_type = FluxType.PDCSAP

            flux = FluxData(
                flux=raw_dataframe["PDCSAP_FLUX"],
                flux_error=raw_dataframe["PDCSAP_FLUX_ERR"],
            )

            reason = (
                "PDCSAP contains the greatest number "
                "of valid cadences."
            )

        else:

            flux_type = FluxType.SAP

            flux = FluxData(
                flux=raw_dataframe["SAP_FLUX"],
                flux_error=raw_dataframe["SAP_FLUX_ERR"],
            )

            reason = (
                "SAP contains the greatest number "
                "of valid cadences."
            )

        return FluxSelectionResult(
            selected_flux_type=flux_type,
            selected_flux=flux,
            selection_method=FluxSelectionMethod.SIMPLE,
            selection_scores=scores,
            metadata={
                "selection_reason": reason,
                "pdcsap_valid": int(pdcsap_score),
                "sap_valid": int(sap_score),
            },
        )