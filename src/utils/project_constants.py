"""
==========================================================
Project Constants
==========================================================

Shared constants used throughout the pipeline.
"""



# PRIMARY KEY

PRIMARY_KEY = "TICID"

DOWNLOADED_COLUMN = "DOWNLOADED"

DOWNLOAD_RETRIES = 3

DOWNLOAD_RETRY_DELAY = 5

PREPROCESSED_COLUMN = "PREPROCESSED"


QUALITY_COLUMN = "QUALITY"

DEFAULT_QUALITY_FLAG = 0


NORMALIZATION_METHOD = "median"


# DETRENDING

DETREND_METHOD = "wotan"

WOTAN_METHOD = "biweight"

WOTAN_BREAK_TOLERANCE = 0.5

WOTAN_EDGE_CUTOFF = 0.0

WOTAN_WINDOW_LENGTH = 0.75


# TESS DOWNLOAD SETTINGS

DEFAULT_TESS_MISSION = "TESS"

DEFAULT_TESS_AUTHOR = "SPOC"

DEFAULT_TESS_CADENCE = 120


# VERSION DATA

PIPELINE_VERSION = "2.0.0"

PREPROCESS_VERSION = "1.0.0"
PREPROCESS_PIPELINE_NAME = "preprocess_lightcurve"














# LABEL PRIORITY

LABEL_PRIORITY = {

    "CP": 1,

    "KP": 2,

    "FP": 3,

    "FA": 4,

    "PC": 5,

    "APC": 6,

    "EB": 7

}



# CLASS DIRECTORY MAPPING

CLASS_DIRECTORY = {

    "Planet": "planets",

    "Candidate": "candidates",

    "False Positive": "false_positives",

    "Eclipsing Binary": "eclipsing_binaries"

}




# CLASS MAPPING
 

CLASS_MAPPING = {

    "CP": "Planet",

    "KP": "Planet",

    "FP": "False Positive",

    "FA": "False Positive",

    "PC": "Candidate",

    "APC": "Candidate",

    "EB": "Eclipsing Binary"

}


 
# INITIAL PIPELINE STATUS
 

INITIAL_PIPELINE_STATUS = {

    "DOWNLOADED": False,

    "PREPROCESSED": False,

    "BLS_COMPLETED": False,

    "FEATURES_EXTRACTED": False,

    "CLASSIFIED": False,

    "FITTED": False

}


 
# MASTER CATALOG COLUMNS
 

# MASTER_COLUMNS = [

#     PRIMARY_KEY,

#     "SOURCE",

#     "CATALOG_LABEL",

#     "PRIMARY_LABEL",

#     "FINAL_CLASS",

#     "LABEL_STATUS",

#     "IS_CONFLICT",

#     "N_SOURCES",

#     "CATALOG_VERSION",

#     "CATALOG_PROCESSED_DATE",

#     "DOWNLOADED",

#     "PREPROCESSED",

#     "BLS_COMPLETED",

#     "FEATURES_EXTRACTED",

#     "CLASSIFIED",

#     "FITTED"

# ]


# MASTER BASE COLUMNS

MASTER_BASE_COLUMNS = [

    PRIMARY_KEY,

    "SOURCE",

    "CATALOG_LABEL",

    "PRIMARY_LABEL",

    "FINAL_CLASS",

    "LABEL_STATUS",

    "IS_CONFLICT",

    "N_SOURCES",

    "CATALOG_VERSION",

    "CATALOG_PROCESSED_DATE"

]

MASTER_COLUMNS = (
    MASTER_BASE_COLUMNS +
    list(INITIAL_PIPELINE_STATUS.keys())
)




# RAW LIGHTCURVE COLUMNS

RAW_LIGHTCURVE_COLUMNS = [

    "time",

    "sap_flux",
    "sap_flux_err",

    "pdcsap_flux",
    "pdcsap_flux_err",

    "quality",

    "psf_centr1",
    "psf_centr2",

    "mom_centr1",
    "mom_centr2"

]


RAW_LIGHTCURVE_COLUMN_MAP = {
    "time": "TIME",
    "sap_flux": "SAP_FLUX",
    "sap_flux_err": "SAP_FLUX_ERR",
    "pdcsap_flux": "PDCSAP_FLUX",
    "pdcsap_flux_err": "PDCSAP_FLUX_ERR",
    "quality": "QUALITY",
    "psf_centr1": "PSF_CENTR1",
    "psf_centr2": "PSF_CENTR2",
    "mom_centr1": "MOM_CENTR1",
    "mom_centr2": "MOM_CENTR2",
}



# PROCESSED LIGHTCURVE SCHEMA

PROCESSED_LIGHTCURVE_COLUMNS = [

    "TICID",

    "SECTOR",

    "TIME",

    "FLUX",

    "FLUX_ERR",

    "QUALITY",

    "MOM_CENTR1",

    "MOM_CENTR2",

]

FINAL_PROCESSED_LIGHTCURVE_COLUMNS = [
    "TICID",
    "SECTOR",
    "TIME",
    "FLUX",
    "FLUX_ERR",
    "QUALITY",
    "MOM_CENTR1",
    "MOM_CENTR2",
    "DETRENDED_FLUX",
    "TREND",
]


RAW_DATASET_COLUMNS = [

    "TICID",

    "SECTOR",

    "TIME",

    "SAP_FLUX",

    "SAP_FLUX_ERR",

    "PDCSAP_FLUX",

    "PDCSAP_FLUX_ERR",

    "QUALITY",

    "PSF_CENTR1",

    "PSF_CENTR2",

    "MOM_CENTR1",

    "MOM_CENTR2"

]


ESSENTIAL_LIGHTCURVE_COLUMNS = [

    "TIME",

    "FLUX",

    "FLUX_ERR"

]

TIMESTAMP_COLUMNS = [

    "SECTOR",

    "TIME"

]



LABEL_DISPLAY_NAMES = {

    "Planet": "Planet",

    "Candidate": "Candidate",

    "False Positive": "False Positive",

    "Eclipsing Binary": "Eclipsing Binary"

}


PIPELINE_LABELS = {

    "Planet",

    "Candidate",

    "False Positive",

    "Eclipsing Binary"

}