"""
==========================================================
Representation Generation Layer (RGL)

Smart flux selector.

Automatically evaluates all available flux
representations and selects the highest-quality
candidate for representation generation.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

import pandas as pd
import numpy as np

from preprocessing.config import (
    PreprocessingConfig,
)

from preprocessing.enums import (
    FluxType,
)

from preprocessing.identifiers import (
    SelectorID,
)

from preprocessing.preprocessing_models import (
    FluxData,
    FluxSelectionResult,
    PreprocessInput,
)

from preprocessing.selectors.selector_base import (
    SelectorPlugin,
)

from preprocessing.constants import (
    TIME_COLUMN,
    DISCOVERABLE_FLUXES,
)



# Internal Models

@dataclass(
    slots=True,
)
class FluxCandidate:
    """
    Internal representation of one selectable
    flux candidate.

    This class is private to SmartSelector and
    should never leave this module.
    """

    flux_type: FluxType

    flux_column: str

    flux_error_column: str

    score: float = 0.0

    metadata: dict[str, float] = field(
        default_factory=dict
    )



# Smart Selector

class SmartSelector(
    SelectorPlugin,
):
    """
    Automatically evaluate and select the best
    available flux representation.
    """

    
    # Plugin Metadata

    @property
    def id(
        self,
    ) -> SelectorID:

        return SelectorID.SMART

    @property
    def name(
        self,
    ) -> str:

        return "Smart Selector"

    @property
    def description(
        self,
    ) -> str:

        return (
            "Automatically evaluates all "
            "available fluxes and selects "
            "the highest-quality candidate."
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

        return {}

    
    # Validation

    def _validate(
        self,
        raw_dataframe: pd.DataFrame,
    ) -> None:
        """
        Validate selector inputs.
        """

        # Empty dataframe

        if raw_dataframe.empty:

            raise ValueError(
                "Cannot select flux from an empty dataframe."
         )

        
        # Must contain at least one column

        if len(raw_dataframe.columns) == 0:

            raise ValueError(
                "Input dataframe contains no columns."
            )

        
        # Must contain TIME

        if TIME_COLUMN not in raw_dataframe.columns:

            raise ValueError(
                f"Missing required column: {TIME_COLUMN}"
            )

    
    # Candidate Discovery

    def _discover_fluxes(
        self,
        raw_dataframe: pd.DataFrame,
    ) -> list[FluxCandidate]:
        """
        Discover all available flux candidates.
        """

        candidates: list[FluxCandidate] = []

        for (

            flux_type,

            flux_column,

            flux_error_column,

        ) in DISCOVERABLE_FLUXES:

            
            # Both columns must exist.

            if (

                flux_column not in raw_dataframe.columns

                or

                flux_error_column not in raw_dataframe.columns

            ):

                continue

            candidates.append(

                FluxCandidate(

                    flux_type=flux_type,

                    flux_column=flux_column,

                    flux_error_column=flux_error_column,

                )

            )

        return candidates



    def _compute_metrics(
        self,
        candidate: FluxCandidate,
        raw_dataframe: pd.DataFrame,
    ) -> dict[str, float]:
        """
        Compute quality metrics.
        """

        # TODO:
        # Extend with additional quality metrics:
        # - uncertainty quality
        # - robust scatter (MAD)
        # - noise estimate
        # - transit preservation

        flux = raw_dataframe[
            candidate.flux_column
        ]

        finite_mask = np.isfinite(flux)

        completeness = float(

            finite_mask.mean()

        )

        return {

            "completeness": completeness,

        }

    
    # Candidate Scoring

    def _score_candidate(
        self,
        candidate: FluxCandidate,
        raw_dataframe: pd.DataFrame,
    ) -> FluxCandidate:
        """
        Score one flux candidate.
        """

        metrics = self._compute_metrics(

            candidate,

            raw_dataframe,

        )

        candidate.metadata.update(

            metrics

        )

        #
        # Version 1
        #

        candidate.score = metrics[
            "completeness"
        ]

        return candidate


    # Ranking

    def _rank_candidates(
        self,
        candidates: list[FluxCandidate],
        raw_dataframe: pd.DataFrame,
    ) -> list[FluxCandidate]:
        """
        Rank all discovered flux candidates.
        """

        scored_candidates = [

            self._score_candidate(

                candidate,

                raw_dataframe,

            )

            for candidate in candidates

        ]

        return sorted(

            scored_candidates,

            key=lambda candidate: candidate.score,

            reverse=True,

        )

    
    # Result Construction

    def _build_result(
        self,
        candidate: FluxCandidate,
        raw_dataframe: pd.DataFrame,
        input_data: PreprocessInput,
    ) -> FluxSelectionResult:
        """
        Build the FluxSelectionResult from the
        selected candidate.
        """

        selected_flux = FluxData(

            flux=raw_dataframe[
                candidate.flux_column
            ],

            flux_error=raw_dataframe[
                candidate.flux_error_column
            ],

            flux_column=candidate.flux_column,

            flux_error_column=candidate.flux_error_column,

        )

        return FluxSelectionResult(

            selected_flux=selected_flux,

            selected_flux_type=candidate.flux_type,

            selection_method=self.id,

            selection_scores={

                candidate.flux_type.value: {

                    "score": candidate.score,

                    **candidate.metadata,

                }

            },

            metadata={

                "selected_flux": candidate.flux_type.value,

                "selected_score": candidate.score,

            },

        )
    

    
    # Public API

    def select(
        self,
        raw_dataframe: pd.DataFrame,
        input_data: PreprocessInput,
        config: PreprocessingConfig,
    ) -> FluxSelectionResult:
        """
        Select the highest-quality flux
        representation.
        """

        self._validate(
            raw_dataframe,
        )

        candidates = self._discover_fluxes(
            raw_dataframe,
        )

        if not candidates:

            raise ValueError(
                "No valid flux candidates found."
            )

        ranked_candidates = self._rank_candidates(
            candidates,
            raw_dataframe,
        )


        return self._build_result(
            ranked_candidates[0],
            raw_dataframe,
            input_data,
        )