"""
==========================================================
Representation Generation Layer (RGL)

Enums used throughout the preprocessing framework.

These enums define the common vocabulary shared by the
entire preprocessing package.

Author : Shyam Girish Chinta
==========================================================
"""

from enum import StrEnum


 
# Flux Types

class FluxType(StrEnum):
    """
    Supported flux types.
    """

    SAP = "SAP"

    PDCSAP = "PDCSAP"

    SELECTED = "SELECTED"




# FLUX SELECTION METHOD

class FluxSelectionMethod(StrEnum):
    """
    Flux selection strategy.
    """

    SIMPLE = "simple"

    SMART = "smart"

    AI = "ai"



 
# Representation Types

class RepresentationType(StrEnum):
    """
    Classification of generated representations.
    """

    BASELINE = "baseline"

    EXPERIMENTAL = "experimental"

    OPTIONAL = "optional"


 
# Representation Status

class RepresentationStatus(StrEnum):
    """
    Processing status of a representation.
    """

    CREATED = "created"

    FAILED = "failed"

    SKIPPED = "skipped"


 
# Processing Stages

class ProcessingStage(StrEnum):
    """
    Pipeline stages.

    Used for logging, warnings, timing,
    metadata and error reporting.
    """

    LOAD = "load"

    VALIDATION = "validation"

    FLUX_SELECTION = "flux_selection"

    QUALITY_FILTER = "quality_filter"

    MISSING_VALUE_FILTER = "missing_value_filter"

    REPRESENTATION_GENERATION = "representation_generation"

    REPRESENTATION_METRICS = "representation_metrics"

    REPRESENTATION_COMPARISON = "representation_comparison"

    SAVE = "save"


 
# Warning Severity

class WarningSeverity(StrEnum):
    """
    Severity level for processing warnings.
    """

    INFO = "info"

    WARNING = "warning"

    ERROR = "error"


 
# Transform Categories

class TransformCategory(StrEnum):
    """
    Categories of preprocessing transforms.

    These describe what a transform does,
    not the specific algorithm.
    """

    NORMALIZATION = "normalization"

    DETRENDING = "detrending"

    FILTERING = "filtering"

    SCALING = "scaling"

    CUSTOM = "custom"


 
# Plugin Status

class PluginStatus(StrEnum):
    """
    Availability status of plugins.
    """

    ENABLED = "enabled"

    DISABLED = "disabled"

    EXPERIMENTAL = "experimental"




# PLUGIN TYPE

class PluginType(StrEnum):
    """
    Categories of preprocessing plugins.
    """

    FLUX_SELECTOR = "flux_selector"

    TRANSFORM = "transform"

    METRIC = "metric"

