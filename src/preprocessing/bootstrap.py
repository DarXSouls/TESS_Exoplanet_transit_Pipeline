"""
==========================================================
Representation Generation Layer (RGL)

Bootstrap utilities for the preprocessing framework.

Creates and initializes the default plugin registry.

Author : Shyam Girish Chinta
==========================================================
"""

from __future__ import annotations

from preprocessing.comparison.default_comparison import (
    DefaultComparison,
)
from preprocessing.metrics.default_metric import (
    DefaultMetric,
)
from preprocessing.registry.registry import (
    PluginRegistry,
)

from preprocessing.selectors.simple_selector import (
    SimpleSelector,
)
from preprocessing.selectors.smart_selector import (
    SmartSelector,
)

from preprocessing.transforms.global_median import (
    GlobalMedianTransform,
)

from preprocessing.transforms.wotan_detrend import (
    WotanDetrendTransform,
)

from preprocessing.cleaners.quality_cleaner import (
    QualityCleaner,
)

from preprocessing.cleaners.missing_value_cleaner import (
    MissingValueCleaner,
)
 
# Registry Builder

def build_registry() -> PluginRegistry:
    """
    Build the default preprocessing plugin registry.

    Returns
    -------
    PluginRegistry
        Registry containing all built-in plugins.
    """

    registry = PluginRegistry()

    cleaners = (
        QualityCleaner(),
        MissingValueCleaner(),
    )

    selectors = (
        SimpleSelector(),
        SmartSelector(),
    )
    
    transforms = (
        GlobalMedianTransform(),
        WotanDetrendTransform(),
    )
    
    metrics = (
        DefaultMetric(),
    )
    
    comparisons = (
        DefaultComparison(),
    )



    # Cleaners

    for plugin in cleaners:
        registry.cleaners.register(plugin)

     
    # Selectors   

    for plugin in selectors:
        registry.selectors.register(plugin)

     
    # Transforms

    for plugin in transforms:
        registry.transforms.register(plugin)

     
    # Metrics   

    for plugin in metrics:
        registry.metrics.register(plugin)

     
    # Comparisons

    for plugin in comparisons:
        registry.comparisons.register(plugin)

    return registry