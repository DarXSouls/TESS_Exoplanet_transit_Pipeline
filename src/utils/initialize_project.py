from config import *
from utils.project_constants import *

def initialize_project():

    directories = [

        # RAW
        PLANET_FITS_DIR,
        PLANET_PARQUET_DIR,
        PLANET_METADATA_DIR,

        EB_FITS_DIR,
        EB_PARQUET_DIR,
        EB_METADATA_DIR,

        FP_FITS_DIR,
        FP_PARQUET_DIR,
        FP_METADATA_DIR,

        RAW_SCIENCE_DIR,

        CATALOGS_DIR,

        LOG_DIR,

        # PROCESSED
        PROCESSED_PLANETS_DIR,
        PROCESSED_EB_DIR,
        PROCESSED_FP_DIR,
        PROCESSED_SCIENCE_DIR,


        PROCESSED_SCIENCE_PARQUET_DIR,
        PROCESSED_SCIENCE_METADATA_DIR,

        *PROCESSED_PARQUET_DIRS.values(),
        *PROCESSED_METADATA_DIRS.values(),


        # CANDIDATES
        CANDIDATES_PLANETS_DIR,
        CANDIDATES_EB_DIR,
        CANDIDATES_FP_DIR,
        CANDIDATES_SCIENCE_DIR,

        # FEATURES
        FEATURES_PLANETS_DIR,
        FEATURES_EB_DIR,
        FEATURES_FP_DIR,
        FEATURES_SCIENCE_DIR,

        # FITTING
        TRANSIT_FITS_PLANETS_DIR,
        TRANSIT_FITS_EB_DIR,
        TRANSIT_FITS_FP_DIR,
        TRANSIT_FITS_SCIENCE_DIR,

        # RESULTS
        RESULTS_PLANETS_DIR,
        RESULTS_EB_DIR,
        RESULTS_FP_DIR,
        RESULTS_SCIENCE_DIR,

        # MODELS
        CLASSICAL_MODELS_DIR,
        DEEP_MODELS_DIR,
        ENSEMBLE_MODELS_DIR,

        # PLOTS
        RAW_PLOTS_DIR,
        DETRENDED_PLOTS_DIR,
        BLS_PLOTS_DIR,
        FOLDED_PLOTS_DIR,
        TRANSIT_FIT_PLOTS_DIR,
        FINAL_CANDIDATE_PLOTS_DIR,

        # REPORTS
        CANDIDATE_REPORTS_DIR,
        SECTOR_REPORTS_DIR,
        FINAL_SUBMISSION_DIR
    ]

    for directory in directories:
        directory.mkdir(
            parents=True,
            exist_ok=True
        )

    print("Project structure verified.")