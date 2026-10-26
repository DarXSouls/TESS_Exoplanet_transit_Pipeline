from pathlib import Path


# PROJECT ROOT

PROJECT_ROOT = Path(__file__).resolve().parent.parent



# RAW DATA

RAW_DIR = PROJECT_ROOT / "data" / "raw"



# Training data

RAW_PLANETS_DIR = RAW_DIR / "planets"
RAW_EB_DIR = RAW_DIR / "eclipsing_binaries"
RAW_FP_DIR = RAW_DIR / "false_positives"


# Science data

RAW_SCIENCE_DIR = RAW_DIR / "science_sector"




# RAW subfolders

PLANET_FITS_DIR = RAW_PLANETS_DIR / "fits"
PLANET_PARQUET_DIR = RAW_PLANETS_DIR / "parquet"
PLANET_METADATA_DIR = RAW_PLANETS_DIR / "metadata"

EB_FITS_DIR = RAW_EB_DIR / "fits"
EB_PARQUET_DIR = RAW_EB_DIR / "parquet"
EB_METADATA_DIR = RAW_EB_DIR / "metadata"

FP_FITS_DIR = RAW_FP_DIR / "fits"
FP_PARQUET_DIR = RAW_FP_DIR / "parquet"
FP_METADATA_DIR = RAW_FP_DIR / "metadata"




# Processed data

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_PLANETS_DIR = PROCESSED_DIR / "planets"
PROCESSED_EB_DIR = PROCESSED_DIR / "eclipsing_binaries"
PROCESSED_FP_DIR = PROCESSED_DIR / "false_positives"
PROCESSED_SCIENCE_DIR = PROCESSED_DIR / "science_sector"

PROCESSED_CANDIDATE_DIR = (
    PROCESSED_DIR / "candidates"
)


# Processed subfolders

PROCESSED_SCIENCE_PARQUET_DIR = (
    PROCESSED_SCIENCE_DIR / "parquet"
)

PROCESSED_SCIENCE_METADATA_DIR = (
    PROCESSED_SCIENCE_DIR / "metadata"
)


PROCESSED_PARQUET_DIRS = {

    "Planet": PROCESSED_PLANETS_DIR / "parquet",

    "Candidate": PROCESSED_CANDIDATE_DIR / "parquet",

    "False Positive": PROCESSED_FP_DIR / "parquet",

    "Eclipsing Binary": PROCESSED_EB_DIR / "parquet",

}

PROCESSED_METADATA_DIRS = {

    "Planet": PROCESSED_PLANETS_DIR / "metadata",

    "Candidate": PROCESSED_CANDIDATE_DIR / "metadata",

    "False Positive": PROCESSED_FP_DIR / "metadata",

    "Eclipsing Binary": PROCESSED_EB_DIR / "metadata",

}




# Candidates - BLS outputs

CANDIDATES_DIR = PROJECT_ROOT / "data" / "candidates"

CANDIDATES_PLANETS_DIR = CANDIDATES_DIR / "planets"
CANDIDATES_EB_DIR = CANDIDATES_DIR / "eclipsing_binaries"
CANDIDATES_FP_DIR = CANDIDATES_DIR / "false_positives"
CANDIDATES_SCIENCE_DIR = CANDIDATES_DIR / "science_sector"





# Features

FEATURES_DIR = PROJECT_ROOT / "data" / "features"

FEATURES_PLANETS_DIR = FEATURES_DIR / "planets"
FEATURES_EB_DIR = FEATURES_DIR / "eclipsing_binaries"
FEATURES_FP_DIR = FEATURES_DIR / "false_positives"
FEATURES_SCIENCE_DIR = FEATURES_DIR / "science_sector"




# Transit fitting outputs

TRANSIT_FITS_DIR = PROJECT_ROOT / "data" / "fits"

TRANSIT_FITS_PLANETS_DIR = TRANSIT_FITS_DIR / "planets"
TRANSIT_FITS_EB_DIR = TRANSIT_FITS_DIR / "eclipsing_binaries"
TRANSIT_FITS_FP_DIR = TRANSIT_FITS_DIR / "false_positives"
TRANSIT_FITS_SCIENCE_DIR = TRANSIT_FITS_DIR / "science_sector"




# Final results

RESULTS_DIR = PROJECT_ROOT / "data" / "results"

RESULTS_PLANETS_DIR = RESULTS_DIR / "planets"
RESULTS_EB_DIR = RESULTS_DIR / "eclipsing_binaries"
RESULTS_FP_DIR = RESULTS_DIR / "false_positives"
RESULTS_SCIENCE_DIR = RESULTS_DIR / "science_sector"




# Catalogs

CATALOGS_DIR = PROJECT_ROOT / "data" / "catalogs"

RAW_CATALOGS_DIR = CATALOGS_DIR / "raw"

PROCESSED_CATALOGS_DIR = CATALOGS_DIR / "processed"

PLANETS_CATALOG = (
    CATALOGS_DIR /
    "planets_catalog.csv"
)

EB_CATALOG = (
    CATALOGS_DIR /
    "eclipsing_binaries_catalog.csv"
)

FP_CATALOG = (
    CATALOGS_DIR /
    "false_positives_catalog.csv"
)

MASTER_CATALOG = (
    CATALOGS_DIR /
    "master_catalog.csv"
)



# LOG FILES

LOG_DIR = PROJECT_ROOT / "data" / "logs"

DOWNLOAD_LOG_FILE = LOG_DIR / "download_log.csv"

PREPROCESS_LOG_FILE = (
    LOG_DIR / "preprocess_log.csv"
)




# Models

MODELS_DIR = PROJECT_ROOT / "models"

CLASSICAL_MODELS_DIR = MODELS_DIR / "classical"
DEEP_MODELS_DIR = MODELS_DIR / "deep_learning"
ENSEMBLE_MODELS_DIR = MODELS_DIR / "ensemble"



# Plots

PLOTS_DIR = PROJECT_ROOT / "plots"

RAW_PLOTS_DIR = PLOTS_DIR / "raw"
DETRENDED_PLOTS_DIR = PLOTS_DIR / "detrended"
BLS_PLOTS_DIR = PLOTS_DIR / "bls"
FOLDED_PLOTS_DIR = PLOTS_DIR / "folded"
TRANSIT_FIT_PLOTS_DIR = PLOTS_DIR / "transit_fits"
FINAL_CANDIDATE_PLOTS_DIR = PLOTS_DIR / "final_candidates"




# Reports

REPORTS_DIR = PROJECT_ROOT / "reports"

CANDIDATE_REPORTS_DIR = REPORTS_DIR / "candidate_reports"
SECTOR_REPORTS_DIR = REPORTS_DIR / "sector_reports"
FINAL_SUBMISSION_DIR = REPORTS_DIR / "final_submission"