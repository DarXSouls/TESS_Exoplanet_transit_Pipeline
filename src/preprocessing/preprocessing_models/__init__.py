"""
Public exports for preprocessing models.

Plugin implementations should import models from this
package rather than individual modules.
"""

# Input Models

from preprocessing.preprocessing_models.input_models import (
    FluxData,
    FluxSelectionResult,
    PreprocessInput,
)

# Representation Models

from preprocessing.preprocessing_models.representation_models import (
    Representation,
    RepresentationColumns,
    TransformStep,
)

# Metric Models

from preprocessing.preprocessing_models.metrics_models import (
    RepresentationComparison,
    RepresentationMetrics,
)

# Result Models

from preprocessing.preprocessing_models.result_models import (
    PreprocessResult,
)

# Statistics Models

from preprocessing.preprocessing_models.statistics_models import (
    PipelineStatistics,
    PluginStatistics,
    ProcessingError,
    ProcessingStatistics,
    ProcessingWarning,
)

__all__ = [
    # Input
    "FluxData",
    "FluxSelectionResult",
    "PreprocessInput",

    # Representation
    "Representation",
    "RepresentationColumns",
    "TransformStep",

    # Metrics
    "RepresentationMetrics",
    "RepresentationComparison",

    # Results
    "PreprocessResult",

    # Statistics
    "ProcessingStatistics",
    "PipelineStatistics",
    "PluginStatistics",
    "ProcessingWarning",
    "ProcessingError",
]