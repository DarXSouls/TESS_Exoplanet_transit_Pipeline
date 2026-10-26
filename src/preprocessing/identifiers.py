"""
==========================================================
Representation Generation Layer (RGL)

Plugin identifiers used throughout the preprocessing
framework.

Author : Shyam Girish Chinta
==========================================================
"""

from enum import StrEnum


 
# Flux Selectors

class SelectorID(StrEnum):

    SIMPLE = "SIMPLE"

    SMART = "SMART"


 
# Transforms

class TransformID(StrEnum):

    GLOBAL_MEDIAN = "GLOBAL_MEDIAN"

    WOTAN_DETREND = "WOTAN_DETREND"

    LOCAL_MEDIAN = "LOCAL_MEDIAN"

    ROBUST_SCALE = "ROBUST_SCALE"

    DEPTH_SCALE = "DEPTH_SCALE"

    LIGHTKURVE = "LIGHTKURVE"

    GAUSSIAN_PROCESS = "GAUSSIAN_PROCESS"


 
# Metrics 

class MetricID(StrEnum):

    DEFAULT = "DEFAULT"

    RMS = "RMS"

    MAD = "MAD"

    CDPP_PROXY = "CDPP_PROXY"

    SKEWNESS = "SKEWNESS"

    KURTOSIS = "KURTOSIS"

    OUTLIER_FRACTION = "OUTLIER_FRACTION"

    TRANSIT_PRESERVATION = "TRANSIT_PRESERVATION"


 
# Comparison

class ComparisonID(StrEnum):

    DEFAULT = "DEFAULT"

    WEIGHTED = "WEIGHTED"

    AI = "AI"


class CleanerID(StrEnum):

    QUALITY = "quality"

    MISSING_VALUES = "missing_values"