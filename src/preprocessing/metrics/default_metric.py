"""
==========================================================
Representation Generation Layer (RGL)

Default statistical metric plugin.

Computes basic statistical properties for a scientific
representation.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import numpy as np
import pandas as pd

from preprocessing.config import PreprocessingConfig
from preprocessing.identifiers import MetricID
from preprocessing.metrics.metric_base import MetricPlugin
from preprocessing.preprocessing_models.metrics_models import (
    RepresentationMetrics,
)
from preprocessing.preprocessing_models.representation_models import (
    Representation,
)


 
# Default Metric

class DefaultMetric(MetricPlugin):
    """
    Computes basic statistical metrics for a
    representation.
    """

    @property
    def id(self) -> MetricID:
        return MetricID.DEFAULT

    @property
    def name(self) -> str:
        return "Default Metric"

    @property
    def description(self) -> str:
        return (
            "Computes baseline statistical metrics."
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

    def evaluate(
        self,
        cleaned_dataframe: pd.DataFrame,
        representation: Representation,
        config: PreprocessingConfig,
    ) -> RepresentationMetrics:
        """
        Compute statistical metrics for a representation.
        """

        flux = representation.columns.columns[
            representation.primary_flux_column
        ]

        values = flux.to_numpy(dtype=float)

        valid = values[~np.isnan(values)]

        metrics = {

            "n_samples":
                float(values.size),

            "n_valid":
                float(valid.size),

            "n_missing":
                float(values.size - valid.size),

            "mean":
                float(np.nanmean(values)),

            "median":
                float(np.nanmedian(values)),

            "std":
                float(np.nanstd(values)),

            "mad":
                float(
                    np.nanmedian(
                        np.abs(
                            values -
                            np.nanmedian(values)
                        )
                    )
                ),

            "rms":
                float(
                    np.sqrt(
                        np.nanmean(
                            values ** 2
                        )
                    )
                ),

            "minimum":
                float(np.nanmin(values)),

            "maximum":
                float(np.nanmax(values)),
        }

        return RepresentationMetrics(

            representation_id=
                representation.representation_id,

            metrics=metrics,

            quality_score=None,

            evaluation_method="default",

            evaluation_version=(1, 0, 0),
        )