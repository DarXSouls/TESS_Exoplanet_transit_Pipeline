"""
==========================================================
Representation Generation Layer (RGL)

Top-level registry used by the preprocessing framework.

This class aggregates all specialised plugin registries
into a single access point used by the preprocessing
pipeline.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from preprocessing.registry.comparison_registry import (
    ComparisonRegistry,
)
from preprocessing.registry.metric_registry import (
    MetricRegistry,
)
from preprocessing.registry.selector_registry import (
    SelectorRegistry,
)
from preprocessing.registry.transform_registry import (
    TransformRegistry,
)
from preprocessing.registry.cleaner_registry import (
    CleanerRegistry,
)


 
# Plugins Registry

@dataclass(
    slots=True,
    frozen=True,
)
class PluginRegistry:
    """
    Top-level plugin registry.

    This class aggregates all specialised registries into
    one immutable container. Individual registries remain
    mutable through their own registration APIs.

    Notes
    -----
    The Registry itself is immutable. Plugin registration
    occurs through the contained specialised registries.
    """

    cleaners: CleanerRegistry = field(
        default_factory=CleanerRegistry
    )

    selectors: SelectorRegistry = field(
        default_factory=SelectorRegistry
    )

    transforms: TransformRegistry = field(
        default_factory=TransformRegistry
    )

    metrics: MetricRegistry = field(
        default_factory=MetricRegistry
    )

    comparisons: ComparisonRegistry = field(
        default_factory=ComparisonRegistry
    )

    
    # Convenience Properties

    @property
    def n_cleaners(self) -> int:
        """
        Number of registered cleaner plugins.
        """

        return len(self.cleaners)

    @property
    def n_selectors(self) -> int:
        """
        Number of registered selector plugins.
        """

        return len(self.selectors)

    @property
    def n_transforms(self) -> int:
        """
        Number of registered transform plugins.
        """

        return len(self.transforms)

    @property
    def n_metrics(self) -> int:
        """
        Number of registered metric plugins.
        """

        return len(self.metrics)

    @property
    def n_comparisons(self) -> int:
        """
        Number of registered comparison plugins.
        """

        return len(self.comparisons)

    @property
    def total_plugins(self) -> int:
        """
        Total number of registered plugins.
        """

        return (
            self.n_cleaners
            + self.n_selectors
            + self.n_transforms
            + self.n_metrics
            + self.n_comparisons
        )