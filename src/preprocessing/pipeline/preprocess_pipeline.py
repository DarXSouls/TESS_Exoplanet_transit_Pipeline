"""
==========================================================
Representation Generation Layer (RGL)

Plugin-driven preprocessing pipeline.

This pipeline orchestrates the execution of preprocessing
plugins without containing any scientific algorithms.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations


import pandas as pd

from preprocessing.config import PreprocessingConfig
from preprocessing.preprocessing_models.input_models import (
    PreprocessInput,
)
from preprocessing.preprocessing_models.result_models import (
    PreprocessResult,
)
from preprocessing.registry.registry import (
    PluginRegistry,
)

from preprocessing.preprocessing_models.input_models import (
    FluxSelectionResult,
)

from preprocessing.preprocessing_models.metrics_models import (
    RepresentationMetrics,
)

from preprocessing.preprocessing_models.representation_models import (
    Representation,
)

from preprocessing.preprocessing_models.metrics_models import (
    RepresentationComparison,
)


 
# Preprocess Pipeline

class PreprocessPipeline:
    """
    Plugin-driven preprocessing pipeline.

    Responsibilities
    ----------------
    * Load input data.
    * Validate dataframe.
    * Execute cleaner plugins.
    * Execute selector plugins.
    * Execute transform plugins.
    * Execute metric plugins.
    * Execute comparison plugins.
    * Construct a PreprocessResult.

    This class intentionally contains no scientific
    preprocessing algorithms. Those belong exclusively
    to plugins.
    """

     
    # Constructor
     

    def __init__(
        self,
        registry: PluginRegistry,
        config: PreprocessingConfig,
    ) -> None:

        self._registry = registry
        self._config = config

     
    # Public API
     

    def run(
        self,
        input_data: PreprocessInput,
    ) -> PreprocessResult:
        """
        Execute the preprocessing pipeline for one target.

        Parameters
        ----------
        input_data
            Input information describing one target.

        Returns
        -------
        PreprocessResult
            Complete preprocessing result.
        """


         
        # Load data

        raw_dataframe = self._load_dataframe(
            input_data
        )

         
        # Validation

        validated_dataframe = self._validate_dataframe(
            raw_dataframe
        )

        cleaned_dataframe = self._clean_dataframe(
            validated_dataframe
        )

         
        # Flux Selection

        flux_selection = self._select_flux(
            cleaned_dataframe,
            input_data,
        )

         
        # Representation Generation

        representations = self._generate_representations(
            cleaned_dataframe,
            flux_selection,
        )

         
        # Representation Evaluation

        representation_metrics = (
            self._evaluate_representations(
                cleaned_dataframe,
                representations,
            )
        )

         
        # Representation Comparison

        comparison = (
            self._compare_representations(
                representation_metrics
            )
        )


         
        # Finalize

        return self._build_result(

            input_data=input_data,
            cleaned_dataframe=cleaned_dataframe,
            flux_selection=flux_selection,
            representations=representations,
            representation_metrics=representation_metrics,
            comparison=comparison,
        )

     
    # Data Loading
     

    def _load_dataframe(
        self,
        input_data: PreprocessInput,
    ) -> pd.DataFrame:
        """
        Load the raw light curve dataframe.

        Parameters
        ----------
        input_data
            Pipeline input.

        Returns
        -------
        pd.DataFrame
            Raw dataframe loaded from disk.
        """

        return pd.read_parquet(
            input_data.parquet_file
        )

     
    # Validation

    def _validate_dataframe(
        self,
        raw_dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Validate the dataframe before plugin execution.

        Notes
        -----
        Validation is intentionally lightweight for V2.

        Future versions will delegate validation to a
        dedicated validator component.

        Returns
        -------
        pd.DataFrame
            Validated dataframe.
        """

        #
        # TODO (V3)
        #
        # - Validate required columns.
        # - Validate dtypes.
        # - Validate time ordering.
        # - Validate duplicate cadences.
        # - Validate quality flags.
        #
        # Replace with
        # DataFrameValidator.validate(...)

        return raw_dataframe



    # CLEANING

    def _clean_dataframe(
        self,
        validated_dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Execute the configured dataframe cleaners.
        """

        cleaned_dataframe = validated_dataframe.copy()

        for cleaner_id in self._config.pipeline.cleaners:

            cleaner = self._registry.cleaners.get(
                cleaner_id
            )

            cleaned_dataframe = cleaner.clean(
                dataframe=cleaned_dataframe,
                config=self._config,
            )

        return cleaned_dataframe


         
    # Flux Selection

    def _select_flux(
        self,
        cleaned_dataframe: pd.DataFrame,
        input_data: PreprocessInput,
    ) -> FluxSelectionResult:
        """
        Execute the configured flux selector.
        """

        selector = self._registry.selectors.get(
            self._config.pipeline.selector
        )

        return selector.select(
            raw_dataframe=cleaned_dataframe,
            input_data=input_data,
            config=self._config,
        )

     
    # Representation Generation

    def _generate_representations(
        self,
        cleaned_dataframe: pd.DataFrame,
        flux_selection: FluxSelectionResult,
    ) -> dict[str, Representation]:
        """
        Generate all configured scientific
        representations.
        """

        representations: dict[
            str,
            Representation,
        ] = {}

        for transform_id in (
            self._config.pipeline.transforms
        ):

            transform = (
                self._registry.transforms.get(
                    transform_id
                )
            )

            representation = transform.transform(
                cleaned_dataframe=cleaned_dataframe,
                flux_selection=flux_selection,
                config=self._config,
            )

            # Prevent duplicate representations.

            if (
                representation.representation_id
                in representations
            ):
                raise ValueError(
                    "Duplicate representation id: "
                    f"{representation.representation_id}"
                )

            representations[
                representation.representation_id
            ] = representation

        return representations

     
    # Representation Evaluation

    def _evaluate_representations(
        self,
        cleaned_dataframe: pd.DataFrame,
        representations: dict[
            str,
            Representation,
        ],
    ) -> dict[
        str,
        RepresentationMetrics,
    ]:
        """
        Evaluate every generated representation.
        """

        metrics: dict[
            str,
            RepresentationMetrics,
        ] = {}

        for metric_id in (
            self._config.pipeline.metrics
        ):

            metric_plugin = (
                self._registry.metrics.get(
                    metric_id
                )
            )

            for (
                representation_id,
                representation,
            ) in representations.items():

                evaluation = (
                    metric_plugin.evaluate(
                        cleaned_dataframe=cleaned_dataframe,
                        representation=representation,
                        config=self._config,
                    )
                )

                # TODO (V3):
                # Support multiple metric plugins
                # per representation.

                metrics[
                    representation_id
                ] = evaluation

        return metrics

         
    # Representation Comparison

    def _compare_representations(
        self,
        representation_metrics: dict[
            str,
            RepresentationMetrics,
        ],
    ) -> RepresentationComparison:
        """
        Compare all evaluated representations and select
        the best one.
        """

        comparison = (
            self._registry.comparisons.get(
                self._config.pipeline.comparison
            )
        )

        return comparison.compare(
            metrics=representation_metrics,
            config=self._config,
        )

     
    # Result Construction

    def _build_result(
        self,
        input_data: PreprocessInput,

        cleaned_dataframe: pd.DataFrame,

        flux_selection: FluxSelectionResult,

        representations: dict[
            str,
            Representation,
        ],

        representation_metrics: dict[
            str,
            RepresentationMetrics,
        ],

        comparison: RepresentationComparison,

    ) -> PreprocessResult:
        """
        Finalize the preprocessing result.

        This method exists to provide a single extension
        point for future versions of the pipeline.

        Future responsibilities may include:

        * execution timing
        * provenance tracking
        * pipeline versioning
        * warnings
        * logging metadata

        Parameters
        ----------

        input_data
            Pipeline input.

        cleaned_dataframe
            Cleaned dataframe after validation and cleaners.

        flux_selection
            Selected flux columns.

        representations
            Generated scientific representations.

        representation_metrics
            Evaluation results for each representation.

        comparison
            Representation comparison result.

        Returns
        -------
        PreprocessResult
            Finalized preprocessing result.
        """

        #
        # V2
        #
        # Nothing additional to do.
        #

        result = PreprocessResult(
            input=input_data,
        )

        result.cleaned_dataframe = cleaned_dataframe

        result.flux_selection = flux_selection

        result.representations.update(
            representations
        )

        result.representation_metrics.update(
            representation_metrics
        )

        result.comparison = comparison

        return result