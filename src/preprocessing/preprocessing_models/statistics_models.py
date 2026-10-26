"""
==========================================================
Representation Generation Layer (RGL)

Statistics models used by the preprocessing framework.

These dataclasses describe execution statistics,
warnings and errors generated during preprocessing.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime

from preprocessing.enums import (
    ProcessingStage,
    WarningSeverity
)


 
# Processing Statistics

@dataclass(
    slots=True,
    frozen=True
)
class ProcessingStatistics:
    """
    Processing statistics for a single target.

    Stores raw execution statistics generated while
    preprocessing one target.
    """

    original_rows: int

    quality_rows_removed: int

    missing_rows_removed: int

    duplicate_rows_removed: int

    final_rows: int

    n_representations_generated: int

    execution_time_seconds: float

    @property
    def total_rows_removed(self) -> int:
        """
        Total removed rows.
        """

        return (
            self.quality_rows_removed
            + self.missing_rows_removed
            + self.duplicate_rows_removed
        )



@dataclass(
    slots=True,
    frozen=True
)
class PluginStatistics:

    execution_time_seconds: float

    n_calls: int

    n_failures: int

    n_skipped: int

 
# Pipeline Statistics

@dataclass(
    slots=True,
    frozen=True
)
class PipelineStatistics:
    """
    Statistics describing one batch preprocessing run.
    """

    targets_processed: int

    targets_succeeded: int

    targets_failed: int

    representations_generated: int

    failed_representations: int

    total_execution_time_seconds: float

    average_target_time_seconds: float

    plugin_statistics: Mapping[
        str,
        PluginStatistics
    ]


 
# Processing Warning
 
@dataclass(
    slots=True,
    frozen=True
)
class ProcessingWarning:
    """
    Recoverable warning generated during preprocessing.
    """

    stage: ProcessingStage

    severity: WarningSeverity

    message: str

    tic_id: int | None = None

    plugin_name: str | None = None

    timestamp: datetime | None = None


 
# Processing Error

@dataclass(
    slots=True,
    frozen=True
)
class ProcessingError:
    """
    Non-recoverable preprocessing error.
    """

    stage: ProcessingStage

    message: str

    tic_id: int | None = None

    plugin_name: str | None = None

    timestamp: datetime | None = None