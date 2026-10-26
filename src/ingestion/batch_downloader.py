"""
==========================================================
Batch Downloader
==========================================================

Downloads TESS light curves using the Master Catalog.

Responsibilities
----------------
- Read Master Catalog
- Filter targets
- Determine output folders
- Download light curves
- Update pipeline status
- Save download log
==========================================================
"""

from pathlib import Path

from datetime import datetime

import pandas as pd

from tqdm import tqdm

from ingestion.download_tess_v2 import download_tess_target

from utils.project_constants import (

    CLASS_DIRECTORY,

    PRIMARY_KEY,

    DOWNLOADED_COLUMN

)




# LOAD MASTER CATALOG

def load_master_catalog(
    master_catalog_file
):
    """
    Load the master catalog.
    """

    return pd.read_csv(
        master_catalog_file
    )



# FILTER TARGETS

def filter_targets(

    master,

    final_class=None,

    label_status=None,

    overwrite=False

):
    """
    Filter targets for downloading.
    """

    dataframe = master.copy()

    if final_class is not None:

        dataframe = dataframe[
            dataframe["FINAL_CLASS"] == final_class
        ]

    if label_status is not None:

        dataframe = dataframe[
            dataframe["LABEL_STATUS"] == label_status
        ]

    if not overwrite:

        dataframe = dataframe[
            ~dataframe[DOWNLOADED_COLUMN]
        ]

    return dataframe




# DETERMINE OUTPUT DIRECTORIES

def get_output_directories(

    raw_directory,

    final_class

):
    """
    Build output directories for a class.
    """

    class_directory = (

        Path(raw_directory)

        /

        CLASS_DIRECTORY[final_class]

    )

    return {

        "fits":

            class_directory / "fits",

        "parquet":

            class_directory / "parquet",

        "metadata":

            class_directory / "metadata"

    }





# UPDATE DOWNLOAD STATUS

def update_pipeline_status(

    master,

    index,

    pipeline_column,

    success

):
    """
    Update download status.
    """

    master.loc[
        index,
        pipeline_column
    ] = success




# SAVE DOWNLOAD LOG

def save_download_log(

    log,

    output_file

):
    """
    Save download log.
    """

    output_file = Path(
        output_file
    )

    output_file.parent.mkdir(

        parents=True,

        exist_ok=True

    )

    pd.DataFrame(
        log
    ).to_csv(

        output_file,

        index=False

    )








# DOWNLOAD DATASET

def download_dataset(

    master_catalog_file,

    raw_directory,

    log_file,

    final_class=None,

    label_status=None,

    overwrite=False,

    stitch=False,

    max_targets = None

):
    """
    Download TESS light curves for targets in the
    master catalog.

    Parameters
    ----------
    master_catalog_file : str or Path

    raw_directory : str or Path

    log_file : str or Path

    final_class : str, optional

    label_status : str, optional

    overwrite : bool, optional

    Returns
    -------
    tuple
        Updated master catalog and download log.
    """

    print()
    print("=" * 42)
    print(" Loading Master Catalog ")
    print("=" * 42)

    master = load_master_catalog(
        master_catalog_file
    )

    print("Filtering Targets...")

    targets = filter_targets(

        master=master,

        final_class=final_class,

        label_status=label_status,

        overwrite=overwrite

    )

    if max_targets is not None:

        targets = targets.head(max_targets)

    print(
        f"Targets Selected : {len(targets)}"
    )

    download_log = []

    class_counts = {

        "Planet": 0,

        "Candidate": 0,

        "False Positive": 0,

        "Eclipsing Binary": 0
    }

    print()
    print("Downloading Targets...")

    for index, row in tqdm(

        targets.iterrows(),

        total=len(targets),

        desc="Downloading"

    ):

        start_time = datetime.now()

        directories = get_output_directories(

            raw_directory=raw_directory,

            final_class=row["FINAL_CLASS"]

        )

        try:

            result = download_tess_target(

                tic_id=row[PRIMARY_KEY],

                fits_directory=directories["fits"],

                parquet_directory=directories["parquet"],

                metadata_directory=directories["metadata"],

                stitch=stitch

            )

            end_time = datetime.now()

            elapsed_seconds = (
                end_time - start_time
            ).total_seconds()


            # ----------------------------------------
            # No downloadable products or lightcurves available
            # ----------------------------------------

            if result is None:

                update_pipeline_status(

                    master=master,

                    index=index,

                    pipeline_column=DOWNLOADED_COLUMN,

                    success=False

                )

                download_log.append({

                    "TICID":
                        row[PRIMARY_KEY],

                    "SOURCE":
                        row["SOURCE"],

                    "FINAL_CLASS":
                        row["FINAL_CLASS"],

                    "LABEL_STATUS":
                        row["LABEL_STATUS"],

                    "STATUS":
                        "NO_DATA",

                    "N_SECTORS":
                        0,
                    
                    "N_ROWS":
                        0,
                    
                    "N_FITS":
                        0,
                    
                    "STITCHED":
                        stitch,
                    
                    "START_TIME":
                        start_time,

                    "END_TIME":
                        end_time,
                    
                    "ELAPSED_SECONDS":
                        round(
                            elapsed_seconds,
                            2
                        ),
                    
                    "ERROR":
                        "No downloadable products found"
                        
                })

                continue

            # ----------------------------------------
            # Successful Download
            # ----------------------------------------

            update_pipeline_status(

                master=master,

                index=index,

                pipeline_column=DOWNLOADED_COLUMN,

                success=True

            )


            class_counts[
                row["FINAL_CLASS"]
            ] += 1



            download_log.append({

                "TICID":
                    row[PRIMARY_KEY],

                "SOURCE":
                    row["SOURCE"],

                "FINAL_CLASS":
                    row["FINAL_CLASS"],

                "LABEL_STATUS":
                    row["LABEL_STATUS"],

                "STATUS":
                    "SUCCESS",
                
                "N_SECTORS":
                    result.selection.n_products,

                "N_ROWS":
                    len(result.dataframe),

                "N_FITS":
                    len(result.fits_files),
                
                "STITCHED":
                    stitch,
                
                "START_TIME":
                    start_time,
                
                "END_TIME":
                    end_time,
                
                "ELAPSED_SECONDS":
                    round(
                        elapsed_seconds,
                        2
                    ),

                "ERROR":
                    None,

            })

        except Exception as error:

            end_time = datetime.now()

            elapsed_seconds = (
                end_time - start_time
            ).total_seconds()

            message = str(error)


            # Error Classification

            if "No products found" in message:

                status = "NO_DATA"
            
            elif "404" in message:

                status = "ARCHIVE_ERROR"
            
            elif (

                "500" in message
                or "502" in message
                or "503" in message
                or "504" in message
                or "Connection" in message
                or "Timeout" in message
                or "Connection reset" in message
            ):
                
                status = "RETRY_FAILED"

            else:

                status = "FAILED"



            update_pipeline_status(

                master=master,

                index=index,

                pipeline_column=DOWNLOADED_COLUMN,

                success=False

            )

            download_log.append({

                "TICID":
                    row[PRIMARY_KEY],

                "SOURCE":
                    row["SOURCE"],

                "FINAL_CLASS":
                    row["FINAL_CLASS"],

                "LABEL_STATUS":
                    row["LABEL_STATUS"],

                "STATUS":
                    status,
                
                "N_SECTORS":
                    None,

                "N_ROWS":
                    None,

                "N_FITS":
                    None,
                
                "STITCHED":
                    stitch,
                
                "START_TIME":
                    start_time,
                
                "END_TIME":
                    end_time,
                
                "ELAPSED_SECONDS":
                    round(
                        elapsed_seconds,
                        2
                    ),

                "ERROR":
                    message,

            })

            print(

                f"\nFailed TIC {row[PRIMARY_KEY]}"

                f"\nstatus : {status}"

                f"\nReason : {error}"

            )

    print()
    print("Saving Master Catalog...")

    master.to_csv(

        master_catalog_file,

        index=False

    )

    print("Saving Download Log...")

    save_download_log(

        download_log,

        log_file

    )

    # ----------------------------------------
    # Statistics
    # ----------------------------------------

    success_count = sum(

        log["STATUS"] == "SUCCESS"

        for log in download_log

    )

    no_data_count = sum(

        log["STATUS"] == "NO_DATA"

        for log in download_log

    )

    archive_error_count = sum(

        log["STATUS"] == "ARCHIVE_ERROR"

        for log in download_log
    )

    retry_failed_count = sum(

        log["STATUS"] == "RETRY_FAILED"

        for log in download_log
    )

    failed_count = sum(

        log["STATUS"] == "FAILED"

        for log in download_log

    )

    print()
    print("=" * 42)
    print(" Download Complete ")
    print("=" * 42)

    print(
        f"Downloaded : {success_count}"
    )

    print()

    for class_name, count in class_counts.items():

        print(
            f"   {class_name:<18}: {count}"
        )
    
    print()

    print(
        f"No Data    : {no_data_count}"
    )

    print(
        f"Archive Error  : {archive_error_count}" 
    )

    print(
        f"Retry Failed   : {retry_failed_count}"
    )

    print(
        f"Failed     : {failed_count}"
    )

    print()

    if download_log:
        
        print(
            f"Success Rate: "
            f"{success_count / len(download_log) * 100:.2f}%"
        )
    
    else:

        print("Success rate: N/A")
        

    print()

    download_log = pd.DataFrame(
        download_log
    )

    if not download_log.empty:
        
        average = download_log["ELAPSED_SECONDS"].mean()
        
        print( 
            f"Average TIME/TIC   : {average:.2f} sec"
        )

    

    return master, download_log


