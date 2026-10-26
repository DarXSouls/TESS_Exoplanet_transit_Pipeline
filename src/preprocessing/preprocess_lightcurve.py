

from pathlib import Path
import json

import pandas as pd
import numpy as np

from datetime import datetime, timezone
import platform

from wotan import flatten

from config import *

from utils.project_constants import (

    RAW_DATASET_COLUMNS,

    PROCESSED_LIGHTCURVE_COLUMNS,

    DEFAULT_QUALITY_FLAG,

    ESSENTIAL_LIGHTCURVE_COLUMNS,

    TIMESTAMP_COLUMNS,

    NORMALIZATION_METHOD,

    DETREND_METHOD,

    WOTAN_METHOD,
    WOTAN_WINDOW_LENGTH,
    WOTAN_BREAK_TOLERANCE,
    WOTAN_EDGE_CUTOFF,

    PREPROCESS_VERSION,
    PREPROCESS_PIPELINE_NAME,

)


from preprocessing.bootstrap import build_registry

from preprocessing.pipeline.preprocess_pipeline import (
    PreprocessPipeline,
)

from preprocessing.config import (
    FrameworkConfig,
    PipelineConfig,
    PreprocessingConfig,
)


from preprocessing.preprocessing_models.input_models import(
    PreprocessInput,
)

from preprocessing.preprocessing_models.result_models import(
    PreprocessResult,
)







# LOAD DATAFRAME

def _load_dataframe(
    preprocess_input: PreprocessInput
) -> PreprocessResult:
    """
    Load the raw light curve dataframe.

    Parameters
    ----------
    preprocess_input : PreprocessInput

    Returns
    -------
    PreprocessResult
    """

    dataframe = pd.read_parquet(
        preprocess_input.parquet_file
    )

    return PreprocessResult(

        input=preprocess_input,

        dataframe=dataframe,

        metadata={},

        steps_completed=[
            "load_dataframe"
        ]

    )




# VALIDATE DATAFRAME

def _validate_dataframe(
    result: PreprocessResult
) -> PreprocessResult:
    """
    Validate the raw light curve dataframe.
    """

    dataframe = result.dataframe

    if dataframe is None:
        raise ValueError(
            "No dataframe loaded."
        )

    if dataframe.empty:
        raise ValueError(
            "Dataframe is empty."
        )

    missing_columns = [

        column

        for column in RAW_DATASET_COLUMNS

        if column not in dataframe.columns

    ]

    if missing_columns:

        raise ValueError(

            "Missing columns: "

            f"{missing_columns}"

        )

    dataframe = dataframe[
        RAW_DATASET_COLUMNS
    ].copy()

    numeric_columns = [

        "TIME",

        "SAP_FLUX",

        "SAP_FLUX_ERR",

        "PDCSAP_FLUX",

        "PDCSAP_FLUX_ERR",

        "QUALITY",

        "MOM_CENTR1",

        "MOM_CENTR2"

    ]

    for column in numeric_columns:

        if not pd.api.types.is_numeric_dtype(
            dataframe[column]
        ):

            raise TypeError(

                f"{column} must be numeric."

            )
        
    
    if dataframe["TICID"].isna().any():

        raise ValueError(
            "TICID contains missing values."
        )
    
    if dataframe["SECTOR"].isna().any():

        raise ValueError(
            "SECTOR contains missing values."
        )
    
    if dataframe["TIME"].isna().any():

        raise ValueError(

            "TIME contains missing values."

        )
    


    if dataframe["TICID"].nunique() != 1:

        raise ValueError(

            "Multiple TICIDs found."

        )
    
    

    for sector, group in dataframe.groupby("SECTOR"):

        if not group["TIME"].is_monotonic_increasing:

            raise ValueError(

                f"Sector {sector} "

                "is not time ordered."

            )

    if dataframe.duplicated(

        subset=[

            "SECTOR",

            "TIME"

        ]

    ).any():

        raise ValueError(

            "Duplicate timestamps found."

        )
    
    
    if result.steps_completed is None:

        result.steps_completed = []

    result.steps_completed.append(
        "validate_dataframe"
    )

    
    result.metadata["validation"] = {

        "tic_id": int(
            dataframe["TICID"].iloc[0]
        ),

        "rows": len(dataframe),

        "columns": len(dataframe.columns),

        "n_sectors": int(
            dataframe["SECTOR"].nunique()
            ),

        "validated": True
    }

    return result



# SELECT FLUX

def _select_flux(
    result: PreprocessResult
) -> PreprocessResult:
    """
    Select the preferred flux columns and convert the
    raw schema into the canonical processed schema.

    Preference
    ----------
    PDCSAP_FLUX
        Preferred corrected flux.

    SAP_FLUX
        Used only if PDCSAP is unavailable.
    """

    dataframe = result.dataframe.copy()

     
    # Select Preferred Flux
     

    pdcsap_valid = dataframe["PDCSAP_FLUX"].notna().sum()
    
    sap_valid = dataframe["SAP_FLUX"].notna().sum()
    
    use_pdcsap = pdcsap_valid >= sap_valid
    
    if use_pdcsap:

        dataframe["FLUX"] = dataframe["PDCSAP_FLUX"]

        dataframe["FLUX_ERR"] = dataframe["PDCSAP_FLUX_ERR"]

        selected_flux = "PDCSAP"

    else:

        dataframe["FLUX"] = dataframe["SAP_FLUX"]

        dataframe["FLUX_ERR"] = dataframe["SAP_FLUX_ERR"]

        selected_flux = "SAP"

     
    # Keep Canonical Columns
     

    dataframe = dataframe[
        PROCESSED_LIGHTCURVE_COLUMNS
    ].copy()

    result.dataframe = dataframe

     
    # Metadata
     

    result.metadata["flux_selection"] = {

        "selected_flux": selected_flux,

        "rows": len(dataframe)

    }

     
    # Processing History
     

    if result.steps_completed is None:

        result.steps_completed = []

    result.steps_completed.append(
        "select_flux"
    )

    return result




# QUALITY FILTER

def _filter_quality(
    result: PreprocessResult
) -> PreprocessResult:
    """
    Remove cadences with non-zero QUALITY flags.
    """

    dataframe = result.dataframe.copy()

    original_rows = len(dataframe)

    dataframe = dataframe[
        dataframe["QUALITY"] == DEFAULT_QUALITY_FLAG
    ].copy()

    filtered_rows = len(dataframe)

    if filtered_rows == 0:

        raise ValueError(
            "No cadences remain after quality filtering."
        )

    removed_rows = original_rows - filtered_rows

    result.dataframe = dataframe

    result.metadata["quality"] = {

        "quality_flag": 0,

        "original_rows": original_rows,

        "removed_rows": removed_rows,

        "remaining_rows": filtered_rows,

        "retained_fraction": round(
            filtered_rows / original_rows,
            4
        ),

        "retained_percentage": round(
            filtered_rows / original_rows * 100,
            2
        )

    }

    if result.steps_completed is None:

        result.steps_completed = []

    result.steps_completed.append(
        "filter_quality"
    )

    return result





# REMOVE MISSING VALUES

def _remove_missing(
    result: PreprocessResult
) -> PreprocessResult:
    """
    Remove invalid cadences containing missing or
    infinite values in the essential light curve
    columns.
    """

    dataframe = result.dataframe.copy()

    original_rows = len(dataframe)

     
    # Replace infinities with NaN
     

    dataframe[
        ESSENTIAL_LIGHTCURVE_COLUMNS
    ] = dataframe[
        ESSENTIAL_LIGHTCURVE_COLUMNS
    ].replace(
        [np.inf, -np.inf],
        np.nan
    )


    missing_rows = dataframe[ESSENTIAL_LIGHTCURVE_COLUMNS].isna().any(axis=1).sum()

     
    # Remove missing essential values
     

    dataframe = dataframe.dropna(

        subset=ESSENTIAL_LIGHTCURVE_COLUMNS

    )



    duplicate_rows = dataframe.duplicated(
        subset=TIMESTAMP_COLUMNS
    ).sum()

     
    # Remove duplicate timestamps
     

    dataframe = dataframe.drop_duplicates(

        subset=TIMESTAMP_COLUMNS

    )

    dataframe = dataframe.reset_index(
        drop=True
    )

    remaining_rows = len(dataframe)

    if remaining_rows == 0:

        raise ValueError(
            "No valid cadences remain after removing missing values."
        )

    removed_rows = original_rows - remaining_rows

    result.dataframe = dataframe

    result.metadata["missing_values"] = {

        "original_rows": original_rows,

        "missing_rows_removed": int(
            missing_rows
        ),

        "duplicates_removed": int(
            duplicate_rows
        ),

        "total_removed": int(
            removed_rows
        ),

        "remaining_rows": remaining_rows,

        "retained_fraction": round(

            remaining_rows / original_rows,

            4

        ),

        "retained_percentage": round(

            remaining_rows / original_rows * 100,

            2

        )

    }

    if result.steps_completed is None:

        result.steps_completed = []

    result.steps_completed.append(
        "remove_missing"
    )

    return result




# NORMALIZE FLUX

def _normalize_flux(
    result: PreprocessResult
) -> PreprocessResult:
    """
    Normalize the light curve using the configured
    normalization method.
    """

    dataframe = result.dataframe.copy()

     
    # Compute normalization factor
     

    if NORMALIZATION_METHOD == "median":

        normalization_factor = dataframe["FLUX"].median()

    else:

        raise ValueError(

            f"Unsupported normalization method: "

            f"{NORMALIZATION_METHOD}"

        )

     
    # Validate normalization factor
     

    if pd.isna(normalization_factor):

        raise ValueError(

            "Normalization factor is NaN."

        )

    if normalization_factor == 0:

        raise ValueError(

            "Normalization factor is zero."

        )

     
    # Normalize Flux
     

    dataframe["FLUX"] = (

        dataframe["FLUX"]

        / normalization_factor

    )

    dataframe["FLUX_ERR"] = (

        dataframe["FLUX_ERR"]

        / normalization_factor

    )

    result.dataframe = dataframe

     
    # Metadata
     

    result.metadata["normalization"] = {

        "method": NORMALIZATION_METHOD,

        "normalization_factor": float(
            normalization_factor
        ),

        "median_flux_after": float(
            dataframe["FLUX"].median()
        ),

        "flux_err_scaled": True

    }

     
    # Processing History
     

    if result.steps_completed is None:

        result.steps_completed = []

    result.steps_completed.append(
        "normalize_flux"
    )

    return result




# DETRENDING ONE SECTOR

def _detrend_sector(
    sector_dataframe: pd.DataFrame
) -> pd.DataFrame:
    """
    Detrend a single TESS sector using
    Wotan Biweight.
    """

    dataframe = sector_dataframe.copy()

    flattened_flux, trend = flatten(

        dataframe["TIME"].to_numpy(),

        dataframe["FLUX"].to_numpy(),

        method=WOTAN_METHOD,

        window_length=WOTAN_WINDOW_LENGTH,

        break_tolerance=WOTAN_BREAK_TOLERANCE,

        edge_cutoff=WOTAN_EDGE_CUTOFF,

        return_trend=True

    )

    dataframe["DETRENDED_FLUX"] = flattened_flux

    dataframe["TREND"] = trend

    if not np.isfinite(
        dataframe["DETRENDED_FLUX"]
    ).all():
        
        raise ValueError(
            "Wotan produced invalid detrended flux values."
        )
    
    if not np.isfinite(
        dataframe["TREND"]
    ).all():
        
        raise ValueError(
            "Wotan produced invalid trend."
        )
    

    return dataframe



# DETRENDING ALL SECTORS

def _detrend_dataframe(
    dataframe: pd.DataFrame
) -> pd.DataFrame:
    """
    Detrend every sector independently.
    """

    detrended = []

    for _, sector in dataframe.groupby("SECTOR"):

        detrended.append(

            _detrend_sector(
                sector
            )

        )

    dataframe = pd.concat(

        detrended,

        ignore_index=True

    )

    dataframe = dataframe.sort_values(

        ["SECTOR", "TIME"]

    ).reset_index(

        drop=True

    )

    return dataframe




# DETRENDING METADATA SAVING

def _detrend(
    result: PreprocessResult
) -> PreprocessResult:
    """
    Detrend the normalized light curve.
    """

    dataframe = _detrend_dataframe(

        result.dataframe

    )

    result.dataframe = dataframe

    result.metadata["detrending"] = {

        "method": DETREND_METHOD,

        "filter": WOTAN_METHOD,

        "window_length_days": WOTAN_WINDOW_LENGTH,

        "break_tolerance": WOTAN_BREAK_TOLERANCE,

        "edge_cutoff": WOTAN_EDGE_CUTOFF,

        "rows": len(dataframe),

        "n_sectors": int(

            dataframe["SECTOR"].nunique()

        )

    }

    if result.steps_completed is None:

        result.steps_completed = []

    result.steps_completed.append(

        "detrend"

    )

    return result




# BUILDING METADATA

def _build_metadata(
    result: PreprocessResult
) -> PreprocessResult:
    """
    Build preprocessing metadata.
    """

    dataframe = result.dataframe

    required_sections = [

        "quality",

        "missing_values",

        "normalization",

        "detrending",

        "validation"
    ]

    for section in required_sections:

        if section not in result.metadata:
            
            raise ValueError(

                f"Missing metadata section: {section}"
            )
    
    result.steps_completed.append(
        "build_metadata"
    )

    metadata = {

        "target": {

            "tic_id": result.input.tic_id,

            "label": result.input.label,

            "catalog": result.input.catalog

        },

        "dataset": {

            "rows": len(dataframe),

            "columns": len(dataframe.columns),

            "column_names": list(
                dataframe.columns
            ),

            "n_sectors": int(
                dataframe["SECTOR"].nunique()
            )

        },

        "validation": result.metadata["validation"],

        "quality": result.metadata[
            "quality"
        ],

        "missing_values": result.metadata[
            "missing_values"
        ],

        "normalization": result.metadata[
            "normalization"
        ],

        "detrending": result.metadata[
            "detrending"
        ],

        "pipeline": {

            "name": PREPROCESS_PIPELINE_NAME,

            "version": PREPROCESS_VERSION,

            "created_utc": datetime.now(
                timezone.utc
            ).isoformat(),

            "python_version": platform.python_version(),

            "steps_completed": result.steps_completed

        }


    }


    result.metadata = metadata


    return result



# BUILD PROCESSED DATAFRAME

def _build_processed_dataframe(
    result: PreprocessResult,
) -> pd.DataFrame:
    """
    Build the final processed dataframe from the
    framework preprocessing result.

    The returned dataframe combines the cleaned
    light curve with the columns generated by the
    selected representation.
    """

    #
    # Validate Result
    #

    if result.cleaned_dataframe is None:

        raise ValueError(
            "No cleaned dataframe available."
        )

    if result.comparison is None:

        raise ValueError(
            "No representation comparison available."
        )

    #
    # Copy cleaned dataframe
    #

    dataframe = result.cleaned_dataframe.copy()

    #
    # Best representation
    #

    best_representation = result.best_representation

    if best_representation is None:

        raise ValueError(
            "No best representation available."
        )

    #
    # Append generated columns
    #

    representation_columns = dict(
        best_representation.columns.columns
    )

    dataframe = dataframe.assign(
        **representation_columns
    )

    return dataframe



# SAVE PARQUET FILES

def _save_parquet(

    result: PreprocessResult,

    overwrite: bool = False

) -> PreprocessResult:
    """
    Save the processed light curve as a parquet file.
    """

     
    # Select Output Directory
     

    if result.input.label is None:
        parquet_directory = PROCESSED_SCIENCE_PARQUET_DIR
    else:
        parquet_directory = PROCESSED_PARQUET_DIRS.get(
            result.input.label
        )
    
    if parquet_directory is None:
        raise ValueError(
            f"Unknown label: {result.input.label}"
        )
    

     
    # TIC Directory
     

    tic_directory = (

        parquet_directory

        / f"TIC_{result.input.tic_id}"

    )

    tic_directory.mkdir(

        parents=True,

        exist_ok=True

    )

     
    # Output File
     

    parquet_file = (

        tic_directory

        / "lightcurve.parquet"

    )

     
    # Skip Existing
     

    if parquet_file.exists() and not overwrite:

        result.parquet_file = parquet_file

        result.steps_completed.append(
            "save_parquet"
        )

        return result

     
    # Save DataFrame
     

    processed_dataframe = (
        _build_processed_dataframe(
            result
        )
    )

    if processed_dataframe.empty:

        raise ValueError(
            "Cannot save an empty dataframe."
        )

    processed_dataframe.to_parquet(
        parquet_file,
        index=False,
    )

     
    # Update Result
     

    result.parquet_file = parquet_file

     
    # Processing History
     

    result.steps_completed.append(

        "save_parquet"

    )

    return result




# SAVE METADATA

def _save_metadata(
    result: PreprocessResult,
    overwrite: bool = False
) -> PreprocessResult:
    """
    Save preprocessing metadata as a JSON file.
    """

     
    # Validate Metadata
     

    if not result.metadata:

        raise ValueError(
            "No metadata available to save."
        )

     
    # Select Output Directory
     

    if result.input.label is None:

        metadata_directory = (
            PROCESSED_SCIENCE_METADATA_DIR
        )

    else:

        metadata_directory = (
            PROCESSED_METADATA_DIRS.get(
                result.input.label
            )
        )

        if metadata_directory is None:

            raise ValueError(
                f"Unknown label: {result.input.label}"
            )

     
    # TIC Directory
     

    tic_directory = (
        metadata_directory
        / f"TIC_{result.input.tic_id}"
    )

    tic_directory.mkdir(
        parents=True,
        exist_ok=True
    )

     
    # Metadata File
     

    metadata_file = (
        tic_directory
        / "metadata.json"
    )

     
    # Skip Existing
     

    if metadata_file.exists() and not overwrite:

        result.metadata_file = metadata_file

        result.steps_completed.append(
            "save_metadata"
        )

        return result

     
    # Save Metadata
     

    with open(
        metadata_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result.metadata,
            file,
            indent=4,
            ensure_ascii=False
        )

     
    # Update Result
     

    result.metadata_file = metadata_file

     
    # Processing History
     

    result.steps_completed.append(
        "save_metadata"
    )

    return result



# PROCESS TARGET

def preprocess_target(
    preprocess_input: PreprocessInput,
    overwrite: bool = False
) -> PreprocessResult:
    """
    Run the complete preprocessing pipeline for a
    single light curve.
    """

    # result = _load_dataframe(
    #     preprocess_input
    # )

    # result = _validate_dataframe(
    #     result
    # )

    # result = _select_flux(
    #     result
    # )

    # result = _filter_quality(
    #     result
    # )

    # result = _remove_missing(
    #     result
    # )

    # result = _normalize_flux(
    #     result
    # )

    framework_config = FrameworkConfig()

    pipeline_config = PipelineConfig()

    config = PreprocessingConfig(
        framework=framework_config,
        pipeline=pipeline_config,
    )

    registry = build_registry()

    pipeline = PreprocessPipeline(
        registry=registry,
        config=config,
    )

    framework_result = pipeline.run(
        preprocess_input
    )

    processed_dataframe = (
        _build_processed_dataframe(
            framework_result
        )
    )





    result = _detrend(
        result
    )

    result = _build_metadata(
        result
    )

    result = _save_parquet(
        result,
        overwrite=overwrite
    )

    result = _save_metadata(
        result,
        overwrite=overwrite
    )

    return result