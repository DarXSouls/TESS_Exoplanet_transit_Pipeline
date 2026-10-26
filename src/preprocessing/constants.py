"""
==========================================================
Representation Generation Layer (RGL)

Framework column names used throughout the preprocessing
pipeline.

Author : Shyam Girish Chinta
==========================================================
"""


from preprocessing.enums import (
    FluxType,
)




# Raw Light Curve Columns

TICID_COLUMN = "TICID"

SECTOR_COLUMN = "SECTOR"

TIME_COLUMN = "TIME"

QUALITY_COLUMN = "QUALITY"

SAP_FLUX_COLUMN = "SAP_FLUX"
SAP_FLUX_ERROR_COLUMN = "SAP_FLUX_ERR"

PDCSAP_FLUX_COLUMN = "PDCSAP_FLUX"
PDCSAP_FLUX_ERROR_COLUMN = "PDCSAP_FLUX_ERR"

PSF_CENTR1_COLUMN = "PSF_CENTR1"
PSF_CENTR2_COLUMN = "PSF_CENTR2"

MOM_CENTR1_COLUMN = "MOM_CENTR1"
MOM_CENTR2_COLUMN = "MOM_CENTR2"



FLUX_COLUMN = "FLUX"

FLUX_ERROR_COLUMN = "FLUX_ERR"



# Required Raw Lightcurve Columns

ESSENTIAL_LIGHTCURVE_COLUMNS = (
    TIME_COLUMN,
    QUALITY_COLUMN,
)

TIMESTAMP_COLUMNS = (
    TIME_COLUMN,
)




 
# Global Median Representation

NORMALIZED_FLUX_COLUMN = "NORMALIZED_FLUX"

NORMALIZED_FLUX_ERR_COLUMN = "NORMALIZED_FLUX_ERR"


 
# Local Median Representation

LOCAL_NORMALIZED_FLUX_COLUMN = (
    "LOCAL_NORMALIZED_FLUX"
)

LOCAL_NORMALIZED_FLUX_ERR_COLUMN = (
    "LOCAL_NORMALIZED_FLUX_ERR"
)


 
# Robust Scaling Representation

ROBUST_FLUX_COLUMN = "ROBUST_FLUX"

ROBUST_FLUX_ERR_COLUMN = "ROBUST_FLUX_ERR"


 
# Depth Scaling Representation 

DEPTH_SCALED_FLUX_COLUMN = (
    "DEPTH_SCALED_FLUX"
)

DEPTH_SCALED_FLUX_ERR_COLUMN = (
    "DEPTH_SCALED_FLUX_ERR"
)



DETRENDED_FLUX_COLUMN = "DETRENDED_FLUX"

TREND_COLUMN = "TREND"


 
# Wotan Representation 

WOTAN_FLUX_COLUMN = "WOTAN_FLUX"

WOTAN_FLUX_ERR_COLUMN = (
    "WOTAN_FLUX_ERR"
)


 
# Gaussian Process Representation

GP_FLUX_COLUMN = "GP_FLUX"

GP_FLUX_ERR_COLUMN = "GP_FLUX_ERR"



# Available Flux Representations

DISCOVERABLE_FLUXES = (

    (
        FluxType.PDCSAP,
        PDCSAP_FLUX_COLUMN,
        PDCSAP_FLUX_ERROR_COLUMN,
    ),

    (
        FluxType.SAP,
        SAP_FLUX_COLUMN,
        SAP_FLUX_ERROR_COLUMN,
    ),

)

# Wotan Configuration

WOTAN_METHOD = "biweight"

WOTAN_WINDOW_LENGTH = 0.75

WOTAN_BREAK_TOLERANCE = 0.5

WOTAN_EDGE_CUTOFF = 0.0