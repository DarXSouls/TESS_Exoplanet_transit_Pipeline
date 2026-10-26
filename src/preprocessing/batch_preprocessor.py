from dataclasses import dataclass, asdict

from pathlib import Path

import time

import pandas as pd

from tqdm import tqdm

from preprocessing.preprocess_lightcurve import (

    PreprocessInput,

    preprocess_target

)

from config import RAW_DIR
from utils.project_constants import LABEL_DISPLAY_NAMES, CLASS_DIRECTORY


@dataclass
class PreprocessLog:
    """
    Processing summary for one target.
    """

    tic_id: int

    label: str

    status: str

    elapsed_seconds: float

    parquet_file: str | None

    metadata_file: str | None

    message: str



# LOAD MASTER CATALOG

def _load_master_catalog(
    master_catalog_file: Path
) -> pd.DataFrame:
    """
    Load the master catalog.
    """

    print()

    print(
        "=========================================="
    )

    print(
        " Loading Master Catalog "
    )

    print(
        "=========================================="
    )

    dataframe = pd.read_csv(
        master_catalog_file
    )

    return dataframe




# FILTERING

def _filter_targets(
    dataframe: pd.DataFrame,
    final_class: str | None = None,
    overwrite: bool = False,
    max_targets: int | None = None
) -> pd.DataFrame:
    """
    Select targets that require preprocessing.
    """

    print("Filtering Targets...")

    targets = dataframe.copy()

     
    # Filter by Class
     

    if final_class is not None:

        targets = targets[
            targets["FINAL_CLASS"] == final_class
        ]


    # ONLY DOWNLOADED TARGETS
    targets = targets[
        targets["DOWNLOADED"] == True
    ]


     
    # Skip Already Processed
     

    if not overwrite:

        targets = targets[
            targets["PREPROCESSED"] == False
        ]

     
    # Limit Targets
     

    if max_targets is not None:

        targets = targets.head(
            max_targets
        )

    print(
        f"Targets Selected : {len(targets)}"
    )

    print()

    return targets.reset_index(
        drop=True
    )




# UPDATING PREPROCESS STATUS

def _update_preprocess_status(
    master_catalog: pd.DataFrame,
    tic_id: int,
    status: bool
) -> pd.DataFrame:
    """
    Update preprocessing status for one target.
    """

    mask = (
        master_catalog["TICID"] == tic_id
    )

    if not mask.any():

        raise ValueError(
            f"TIC {tic_id} not found in master catalog."
        )

    master_catalog.loc[
        mask,
        "PREPROCESSED"
    ] = status

    return master_catalog



# SAVE MASTER CATALOG

def _save_master_catalog(
    master_catalog: pd.DataFrame,
    master_catalog_file: Path
) -> None:
    """
    Save the updated master catalog.
    """


    master_catalog.to_csv(
        master_catalog_file,
        index=False
    )



# SAVE PREPROCESS LOG

def _save_preprocess_log(
    preprocess_log: list[PreprocessLog],
    log_file: Path
) -> None:
    """
    Save preprocessing log.
    """

    if not preprocess_log:

        print(
            "No preprocessing log to save."
        )

        return

    print("Saving Preprocessing Log...")

    log_dataframe = pd.DataFrame(

        [
            asdict(log)
            for log in preprocess_log
        ]

    )

    log_file.parent.mkdir(
        
        parents=True,

        exist_ok=True
    )


    log_dataframe.to_csv(

        log_file,

        index=False

    )





# PRINT SUMMARY

def _print_summary(
    preprocess_log: list[PreprocessLog]
) -> None:
    """
    Print preprocessing summary.
    """

     
    # Empty Log
     

    if not preprocess_log:

        print()

        print(
            "No preprocessing summary available."
        )

        return

     
    # Create Summary DataFrame
     

    summary = pd.DataFrame(

        [
            asdict(log)
            for log in preprocess_log
        ]

    )

     
    # Status Counts
     

    completed_targets = summary[
        summary["status"] == "COMPLETED"
    ]

    completed = len(completed_targets)

    failed = (
        summary["status"] == "FAILED"
    ).sum()

    skipped = (
        summary["status"] == "SKIPPED"
    ).sum()

     
    # Class Counts 
     

    class_counts = (
        completed_targets["label"]
        .value_counts()
    )

     
    # Statistics
     

    success_rate = (
        (completed / len(summary)) * 100
        if len(summary) > 0
        else 0.0
    ) 

    average_time = (
        completed_targets[
            "elapsed_seconds"
        ].mean()
    )

    if pd.isna(
        average_time
    ):

        average_time = 0.0

     
    # Print Summary
     

    print()

    print(
        "=========================================="
    )

    print(
        " Preprocessing Complete "
    )

    print(
        "=========================================="
    )

    print(
        f"Processed : {completed}"
    )

    print()

    for label, display_name in LABEL_DISPLAY_NAMES.items():

        count = class_counts.get(
            label,
            0
        )

        print(
            f"   {display_name:<18}: {count}"
        )

    print()

    print(
        f"Skipped           : {skipped}"
    )

    print(
        f"Failed            : {failed}"
    )

    print()

    print(
        f"Success Rate      : "
        f"{success_rate:.2f}%"
    )

    print()

    print(
        f"Average Time/TIC  : "
        f"{average_time:.2f} sec"
    )

    print()




# PREPROCESS DATASET

def preprocess_dataset(
    master_catalog_file: Path,
    log_file: Path,
    final_class: str | None = None,
    overwrite: bool = False,
    max_targets: int | None = None
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Preprocess a batch of downloaded light curves.
    """

     
    # Load Master Catalog
     

    master_catalog = _load_master_catalog(
        master_catalog_file
    )

     
    # Filter Targets
     

    targets = _filter_targets(
        dataframe=master_catalog,
        final_class=final_class,
        overwrite=overwrite,
        max_targets=max_targets
    )

     
    # Processing Log
     

    preprocess_log: list[PreprocessLog] = []

     
    # Process Targets
     

    print("Preprocessing Targets...")

    for _, target in tqdm(
        targets.iterrows(),
        total=len(targets),
        desc="Preprocessing"
    ):

        start_time = time.perf_counter()

        try:

            # -----------------------------
            # Build Input
            # -----------------------------

            tic_id = int(
                target["TICID"]
            )

            label = target["FINAL_CLASS"]

            class_directory = CLASS_DIRECTORY[label]

            parquet_file = (
                 RAW_DIR
                 / class_directory
                 / "parquet"
                 / f"TIC_{tic_id}"
                 / "lightcurve.parquet"
            )

            preprocess_input = PreprocessInput(

                tic_id=tic_id,

                label=label,

                catalog=target["SOURCE"],

                parquet_file=parquet_file,

            )

            # -----------------------------
            # Run Pipeline
            # -----------------------------

            result = preprocess_target(

                preprocess_input,

                overwrite=overwrite

            )

            elapsed = (
                time.perf_counter()
                - start_time
            )

            # -----------------------------
            # Update Master Catalog
            # -----------------------------

            master_catalog = (
                _update_preprocess_status(

                    master_catalog,

                    tic_id=tic_id,

                    status=True

                )
            )

            _save_master_catalog(

                master_catalog,

                master_catalog_file

            )

            # -----------------------------
            # Append Log
            # -----------------------------

            preprocess_log.append(

                PreprocessLog(

                    tic_id=tic_id,

                    label=label,

                    status="COMPLETED",

                    elapsed_seconds=elapsed,

                    parquet_file=str(
                        result.parquet_file
                    ),

                    metadata_file=str(
                        result.metadata_file
                    ),

                    message="Completed"

                )

            )

        except Exception as error:

            elapsed = (
                time.perf_counter()
                - start_time
            )

            print()

            print(
                f"Failed TIC {target['TICID']}"
            )

            print(
                f"Reason : {error}"
            )

            preprocess_log.append(

                PreprocessLog(

                    tic_id=int(
                        target["TICID"]
                    ),

                    label=target["FINAL_CLASS"],

                    status="FAILED",

                    elapsed_seconds=elapsed,

                    parquet_file=None,

                    metadata_file=None,

                    message=str(error)

                )

            )

     
    # Save Outputs
     

    _save_master_catalog(

        master_catalog,

        master_catalog_file

    )

    _save_preprocess_log(

        preprocess_log,

        log_file

    )

    _print_summary(

        preprocess_log

    )

     
    # Return
     

    log_dataframe = pd.DataFrame(

        [
            asdict(log)
            for log in preprocess_log
        ]

    )

    return (

        master_catalog,

        log_dataframe

    )