from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent

SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

print("Project Root:", PROJECT_ROOT)
print("Source Dir:", SRC_DIR)


from config import *
from utils.initialize_project import initialize_project

from catalogs.process_toi_catalog import process_toi_catalog
from catalogs.process_eb_catalog import process_eb_catalog
from catalogs.master_catalog import create_master_catalog

# from utils.project_constants import *

from utils.project_constants import (

    PRIMARY_KEY,

    DOWNLOADED_COLUMN,

    DOWNLOAD_RETRIES,

    DOWNLOAD_RETRY_DELAY,

    DEFAULT_TESS_MISSION,

    DEFAULT_TESS_AUTHOR,

    DEFAULT_TESS_CADENCE,

    PIPELINE_VERSION,

    CLASS_MAPPING,

    LABEL_PRIORITY,

    CLASS_DIRECTORY,

    CLASS_MAPPING,

    INITIAL_PIPELINE_STATUS,

    MASTER_COLUMNS,

    MASTER_BASE_COLUMNS,

    RAW_LIGHTCURVE_COLUMNS,

    RAW_LIGHTCURVE_COLUMN_MAP,

    RAW_DATASET_COLUMNS,

    PROCESSED_LIGHTCURVE_COLUMNS,

    ESSENTIAL_LIGHTCURVE_COLUMNS,

    TIMESTAMP_COLUMNS,

    NORMALIZATION_METHOD,

    DETREND_METHOD,

    WOTAN_METHOD,
    WOTAN_WINDOW_LENGTH,
    WOTAN_BREAK_TOLERANCE,
    WOTAN_EDGE_CUTOFF

)

#from ingestion.batch_downloader import download_dataset

from ingestion.download_tess_v2 import *

from preprocessing.preprocess_lightcurve import *

from preprocessing.batch_preprocessor import *



initialize_project()