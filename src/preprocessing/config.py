"""
==========================================================
Representation Generation Layer (RGL)

Framework configuration used by the preprocessing
pipeline.

These configuration models describe how the framework
should execute without containing any plugin-specific
implementation details.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from preprocessing.identifiers import (
    SelectorID, 
    TransformID,
    MetricID,
    ComparisonID,
    CleanerID
)


 
# Framework Configuration

@dataclass(
    slots=True,
    frozen=True
)
class FrameworkConfig:
    """
    Global framework behaviour.

    These options control how the preprocessing
    framework executes independently of the scientific
    algorithms.
    """

    overwrite: bool = False

    save_parquet: bool = True

    save_metadata: bool = True

    save_logs: bool = True

    parallel_processing: bool = False

    log_level: str = "INFO"


 
# Pipeline Configuration

@dataclass(
    slots=True,
    frozen=True
)
class PipelineConfig:
    """
    Configuration describing one preprocessing pipeline.

    This configuration specifies which plugins should
    execute during preprocessing.

    Plugin-specific parameters are intentionally not
    stored here. Those belong to the plugins
    themselves.
    """

    pipeline_name: str

    selector: SelectorID = SelectorID.SIMPLE

    cleaners: tuple[
        CleanerID,
        ...
    ] = (
        CleanerID.QUALITY,
        CleanerID.MISSING_VALUES,
    )

    transforms: tuple[
        TransformID,
        ...
    ] = (
        TransformID.GLOBAL_MEDIAN,
        TransformID.WOTAN_DETREND,
    )

    metrics: tuple[
        MetricID,
        ...
    ] = (
        MetricID.DEFAULT,
    )

    comparison: ComparisonID = ComparisonID.DEFAULT
    


 
# Preprocessing Configuration

@dataclass(
    slots=True,
    frozen=True
)
class PreprocessingConfig:
    """
    Complete configuration for the preprocessing
    framework.
    """

    framework: FrameworkConfig

    pipeline: PipelineConfig