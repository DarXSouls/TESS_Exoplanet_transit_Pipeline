import json
import shutil

from pathlib import Path

import lightkurve as lk
import numpy as np
import pandas as pd
from numpy.ma import is_masked

import time


from datetime import datetime, timezone
import platform


from lightkurve.search import SearchResult

from ingestion.download_models import (
    ProductSelection,
    DownloadResult,
)

from utils.project_constants import (

    DEFAULT_TESS_MISSION,

    DEFAULT_TESS_AUTHOR,

    DEFAULT_TESS_CADENCE,

    PIPELINE_VERSION,

    RAW_LIGHTCURVE_COLUMNS,

    RAW_LIGHTCURVE_COLUMN_MAP,

    PRIMARY_KEY,

    DOWNLOAD_RETRIES,

    DOWNLOAD_RETRY_DELAY

)

from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class _SelectedProduct:
    """
    Internal helper used while selecting
    the newest product for each sector.
    """

    index: int
    version: int


# _search_lightcurves()

# _extract_sector()

# select_products()

# _download_products()

# _validate_collection()

# _target_directory()

# _save_fits_files()

# _build_dataframe()

# _build_metadata()

# _save_parquet()

# _save_metadata()

# _stitch_lightcurves()










# SEARCH LIGHTCURVES

def _search_lightcurves(

    tic_id: int,

    mission: str | None = None,

    author: str | None = None

) -> SearchResult:
    """
    Search MAST for available light curve products.

    Parameters
    ----------
    tic_id : int
        TESS Input Catalog ID.

    mission : str, optional
        Mission name.

    author : str, optional
        Data provider.

    Returns
    -------
    SearchResult

    Raises
    ------
    ValueError
        If no products are found.
    """

    mission = mission or DEFAULT_TESS_MISSION
    author = author or DEFAULT_TESS_AUTHOR

    search = lk.search_lightcurve(

        target=f"TIC {tic_id}",

        mission=mission,

        author=author

    )

    if len(search) == 0:

        raise ValueError(

            f"No products found for TIC {tic_id}."

        )

    return search





# EXTRACT SECTOR

def _extract_sector(
    mission: str
) -> int:
    """
    Extract sector number from mission string.

    Example
    -------
    "TESS Sector 35"
    
    Returns
    -------
    35

    """

    try:

        return int(

            mission.split()[-1]

        )

    except Exception as exc:

        raise ValueError(

            f"Unable to extract sector from '{mission}'."

        ) from exc






# SELECT PRODUCTS

def _select_products(
    tic_id: int,
    search: SearchResult,
    cadence: int | None = None
) -> ProductSelection:
    """
    Select one product per TESS sector using the requested cadence.

    If multiple products exist for the same sector, the newest
    archive version (highest prvversion) is retained.

    Parameters
    ----------
    tic_id : int
        TESS Input Catalog ID.

    search : SearchResult
        Search results returned by _search_lightcurves().

    cadence : int, optional
        Exposure time (seconds). If None, the project default
        cadence is used.

    Returns
    -------
    ProductSelection
        Selected products ready for download.

    Raises
    ------
    ValueError
        If no matching products are found.
    """

    cadence = cadence or DEFAULT_TESS_CADENCE

    table = search.table

    selected_products: dict[int, _SelectedProduct] = {}

    for index, row in enumerate(table):

        # Keep only requested cadence
        if row["exptime"] != cadence:
            continue

        sector = _extract_sector(row["mission"])

        version = row["prvversion"]

        # Handle missing versions
        if is_masked(version) or version is None:
            version = 0

        previous = selected_products.get(sector)

        if previous is None or version > previous.version:

            selected_products[sector] = _SelectedProduct(
                index=index,
                version=version
            )

    if not selected_products:

        raise ValueError(
            f"No {cadence}s products found for TIC {tic_id}."
        )

    sectors = sorted(selected_products.keys())

    indices = [
        selected_products[sector].index
        for sector in sectors
    ]

    products = search[indices]

    return ProductSelection(

        tic_id=tic_id,

        products=products,

        cadence=cadence,

        sectors=sectors,

        mission=DEFAULT_TESS_MISSION,

        author=products.table["author"][0],

        n_products=len(indices)

    )








# DOWNLOAD PRODUCTS

def _download_products(
    selection: ProductSelection
) -> DownloadResult:
    """
    Download the selected TESS light curve products.

    Parameters
    ----------
    selection : ProductSelection
        Products selected for download.

    Returns
    -------
    DownloadResult
        Downloaded light curves.

    Raises
    ------
    RuntimeError
        If the download fails.
    """

    collection = None

    for attempt in range(DOWNLOAD_RETRIES):

        try:

            collection = selection.products.download_all()

            break

        except Exception as error:

            message = str(error)

            # -----------------------------------------
            # Permanent errors
            # -----------------------------------------

            if (
                "No products found" in message
                or "404" in message
            ):
                raise

            # -----------------------------------------
            # Retryable errors
            # -----------------------------------------

            retryable = (

                "500" in message
                or "502" in message
                or "503" in message
                or "504" in message
                or "Connection" in message
                or "Timeout" in message
                or "Connection reset" in message

            )

            if retryable and attempt < DOWNLOAD_RETRIES - 1:

                print(

                    f"\nRetrying TIC {selection.tic_id} "

                    f"({attempt + 2}/{DOWNLOAD_RETRIES})..."

                )

                time.sleep(
                    DOWNLOAD_RETRY_DELAY
                )

                continue

            raise

    if collection is None:

        raise RuntimeError(
            "Failed to download products."
        )

    if len(collection) != selection.n_products:

        raise ValueError(

            "Downloaded "

            f"{len(collection)} products "

            f"but expected "

            f"{selection.n_products}."

        )

    return DownloadResult(

        selection=selection,

        collection=collection

    )






# VALIDATE COLLECTION

def _validate_collection(
    download: DownloadResult
) -> None:
    """
    Validate the downloaded LightCurveCollection.

    Parameters
    ----------
    download : DownloadResult
        Downloaded products.

    Raises
    ------
    ValueError
        If the collection is invalid.

    FileNotFoundError
        If any downloaded FITS file is missing.
    """

    collection = download.collection

    if collection is None:

        raise ValueError(
            "Downloaded collection is None."
        )

    if len(collection) == 0:

        raise ValueError(
            "Downloaded collection is empty."
        )

    for lc in collection:

        filename = getattr(lc, "filename", None)

        if filename is None:

            raise ValueError(
                "Light curve does not contain a filename."
            )

        filepath = Path(filename)

        if not filepath.exists():

            raise FileNotFoundError(
                filepath
            )

        if not lc.meta:

            raise ValueError(
                f"Missing metadata for {filepath.name}."
            )






# TARGET DIRECTORY

def _target_directory(
    directory: Path,
    tic_id: int
) -> Path:
    """
    Create (if necessary) and return the output
    directory for a TIC target.
    """

    directory = (
        Path(directory)
        / f"TIC_{tic_id}"
    )

    directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return directory




# SAVE FITS FILES

def _save_fits_files(
    download: DownloadResult,
    fits_directory: Path
) -> DownloadResult:
    """
    Copy downloaded FITS files from the Lightkurve cache
    into the project FITS directory.

    Parameters
    ----------
    download : DownloadResult
        Downloaded light curves.

    fits_directory : Path
        Root FITS directory.

    Returns
    -------
    DownloadResult
        Updated download result containing the saved FITS paths.
    """

    tic_id = download.selection.tic_id
    cadence = download.selection.cadence

    output_directory = _target_directory(
        fits_directory,
        tic_id
    )

    saved_files = []

    for sector, lightcurve in zip(
        download.selection.sectors,
        download.collection
    ):

        source = Path(lightcurve.filename)

        if not source.exists():

            raise FileNotFoundError(
                f"Missing cached FITS file:\n{source}"
            )

        destination = (
            output_directory
            /
            f"sector{sector:04d}_{cadence:03d}s.fits"
        )

        shutil.copy2(
            source,
            destination
        )

        saved_files.append(destination)

    return DownloadResult(
        
        selection=download.selection,
        
        collection=download.collection,
        
        fits_files=saved_files,
        
        stitched_lightcurve=download.stitched_lightcurve,
        
        dataframe=download.dataframe,
        
        metadata=download.metadata,
        
        parquet_file=download.parquet_file,
        
        metadata_file=download.metadata_file
        
    )





# BUILD DATAFRAME

def _build_dataframe(
    download: DownloadResult
) -> DownloadResult:
    """
    Build the canonical light curve DataFrame.

    Parameters
    ----------
    download : DownloadResult
        Downloaded light curves.

    Returns
    -------
    DownloadResult
        Updated download result containing the DataFrame.

    Raises
    ------
    ValueError
        If required columns are missing.
    """

    frames = []

    tic_id = download.selection.tic_id

    for lightcurve in download.collection:

        frame = (
            lightcurve.to_pandas()
            .reset_index()
            )
        
        # Validate required columns

        missing_columns = [

            column

            for column in RAW_LIGHTCURVE_COLUMNS

            if column not in frame.columns

        ]

        if missing_columns:

            raise ValueError(

                "Missing columns: "

                f"{missing_columns}"

            )

        frame = frame[
            RAW_LIGHTCURVE_COLUMNS
        ].copy()


        frame = frame.rename(
            columns = RAW_LIGHTCURVE_COLUMN_MAP
        )

        
        # Add provenance columns

        frame.insert(
            0,
            PRIMARY_KEY,
            tic_id
        )

        sector = lightcurve.meta.get("SECTOR")

        if sector is None:

            raise ValueError(
                "Missing SECTOR metadata"
            )
        
        frame.insert(
            1,
            "SECTOR",
            sector
        )



        frames.append(
            frame
        )

    dataframe = pd.concat(

        frames,

        ignore_index=True

    )

    dataframe = dataframe.sort_values(

        "TIME"

    ).reset_index(

        drop=True

    )

    return DownloadResult(

        selection=download.selection,

        collection=download.collection,

        fits_files=download.fits_files,

        stitched_lightcurve=download.stitched_lightcurve,

        dataframe=dataframe,

        metadata=download.metadata,

        parquet_file=download.parquet_file,

        metadata_file=download.metadata_file

    )





# BUILD METADATA

def _build_metadata(
    download: DownloadResult
) -> DownloadResult:
    """
    Build dataset metadata.

    Parameters
    ----------
    download : DownloadResult
        Downloaded dataset.

    Returns
    -------
    DownloadResult
        Updated download result containing metadata.
    """

    dataframe = download.dataframe

    if dataframe is None:

        raise ValueError(
            "DataFrame has not been created."
        )

    
    quality_zero = int(
        (dataframe["QUALITY"] == 0).sum()
    )
    
    quality_nonzero = int(
        (dataframe["QUALITY"] != 0).sum()
        )
    
    total_rows = len(dataframe)
    
    usable_fraction = (
        quality_zero / total_rows
        if total_rows > 0
        else 0.0    
    )
    
    usable_percentage = round(
        usable_fraction * 100,
        2
        )
    

    metadata = {

        
        # TARGET

        "target": {

            "tic_id": download.selection.tic_id,

            "label": None,

            "catalog": "MASTER"

        },

        
        # DOWNLOAD

        "download": {

            "mission": download.selection.mission,

            "author": download.selection.author,

            "cadence": download.selection.cadence,

            "n_sectors": download.selection.n_products,

            "sectors": download.selection.sectors

        },

        
        # DATASET

        "dataset": {

            "rows": total_rows,

            "columns": int(len(dataframe.columns)),

            "column_names": list(dataframe.columns),

            "fits_files": len(download.fits_files)

        },

    
        # QUALITY

        "quality": {

            "valid_rows": quality_zero,

            "flagged_rows": quality_nonzero,

            "usable_fraction": round(
                usable_fraction,
                4
            ),

            "usable_percentage": usable_percentage


        },

        
        # MISSING VALUES

        "missing_values": {

            column: int(count)

            for column, count in dataframe.isna().sum().items()

        },

        
        # PIPELINE

        "pipeline": {

            "version": PIPELINE_VERSION,

            "created_utc": datetime.now(
                timezone.utc
            ).isoformat(),

            "python_version": platform.python_version(),

            "lightkurve_version": lk.__version__

        }

    }

    return DownloadResult(

        selection=download.selection,

        collection=download.collection,

        fits_files=download.fits_files,

        stitched_lightcurve=download.stitched_lightcurve,

        dataframe=download.dataframe,

        metadata=metadata,

        parquet_file=download.parquet_file,

        metadata_file=download.metadata_file

    )





# SAVE PARQUET

def _save_parquet(
    download: DownloadResult,
    parquet_directory: Path
) -> DownloadResult:
    """
    Save the canonical DataFrame as a Parquet file.

    Parameters
    ----------
    download : DownloadResult
        Downloaded dataset.

    parquet_directory : Path
        Root parquet directory.

    Returns
    -------
    DownloadResult
        Updated download result containing the parquet path.
    """

    dataframe = download.dataframe

    if dataframe is None:

        raise ValueError(
            "DataFrame has not been created."
        )

    output_directory = _target_directory(
        parquet_directory,
        download.selection.tic_id
    )

    parquet_file = (

        output_directory

        / "lightcurve.parquet"

    )

    dataframe.to_parquet(

        parquet_file,

        index=False

    )

    return DownloadResult(

        selection=download.selection,

        collection=download.collection,

        fits_files=download.fits_files,

        stitched_lightcurve=download.stitched_lightcurve,

        dataframe=download.dataframe,

        metadata=download.metadata,

        parquet_file=parquet_file,

        metadata_file=download.metadata_file

    )





# SAVE METADATA

def _save_metadata(
    download: DownloadResult,
    metadata_directory: Path
) -> DownloadResult:
    """
    Save dataset metadata as a JSON file.

    Parameters
    ----------
    download : DownloadResult
        Downloaded dataset.

    metadata_directory : Path
        Root metadata directory.

    Returns
    -------
    DownloadResult
        Updated download result containing the metadata file.
    """

    metadata = download.metadata

    if metadata is None:

        raise ValueError(
            "Metadata has not been created."
        )

    output_directory = _target_directory(
        metadata_directory,
        download.selection.tic_id
    )

    metadata_file = (
        output_directory
        / "metadata.json"
    )

    with open(
        metadata_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(

            metadata,

            file,

            indent=4,

            ensure_ascii=False

        )

    return DownloadResult(

        selection=download.selection,

        collection=download.collection,

        fits_files=download.fits_files,

        stitched_lightcurve=download.stitched_lightcurve,

        dataframe=download.dataframe,

        metadata=download.metadata,

        parquet_file=download.parquet_file,

        metadata_file=metadata_file

    )




# STITCH LIGHTCURVES

def _stitch_lightcurves(
    download: DownloadResult
) -> DownloadResult:
    """
    Stitch all downloaded light curves into a single light curve.

    Parameters
    ----------
    download : DownloadResult
        Downloaded dataset.

    Returns
    -------
    DownloadResult
        Updated download result containing the stitched light curve.
    """

    collection = download.collection

    if collection is None:

        raise ValueError(
            "LightCurveCollection has not been downloaded."
        )

    if len(collection) == 0:

        raise ValueError(
            "LightCurveCollection is empty."
        )

    stitched = collection.stitch()

    if len(stitched) == 0:

        raise ValueError(
            "Stitched light curve is empty."
        )

    return DownloadResult(

        selection=download.selection,

        collection=download.collection,

        fits_files=download.fits_files,

        stitched_lightcurve=stitched,

        dataframe=download.dataframe,

        metadata=download.metadata,

        parquet_file=download.parquet_file,

        metadata_file=download.metadata_file

    )




# DOWNLOAD TESS TARGET

def download_tess_target(
    tic_id: int,
    fits_directory: Path,
    parquet_directory: Path,
    metadata_directory: Path,
    cadence: int | None = None,
    mission: str | None = None,
    author: str | None = None,
    stitch: bool = False
) -> DownloadResult:
    """
    Download all available TESS light curves for a target and
    build the canonical raw dataset.

    Parameters
    ----------
    tic_id : int
        TESS Input Catalog ID.

    fits_directory : Path
        Output directory for FITS files.

    parquet_directory : Path
        Output directory for Parquet files.

    metadata_directory : Path
        Output directory for metadata.

    cadence : int, optional
        Requested cadence in seconds.

    mission : str, optional
        Mission name.

    author : str, optional
        Data provider.

    stitch : bool, default=False
        If True, also create a stitched LightCurve.

    Returns
    -------
    DownloadResult
        Complete download result.
    """

    search = _search_lightcurves(
        tic_id=tic_id,
        mission=mission,
        author=author
    )

    selection = _select_products(
        tic_id=tic_id,
        search=search,
        cadence=cadence
    )

    download = _download_products(
        selection
    )

    _validate_collection(
        download
    )

    download = _save_fits_files(
        download,
        fits_directory
    )

    download = _build_dataframe(
        download
    )

    download = _build_metadata(
        download
    )

    download = _save_parquet(
        download,
        parquet_directory
    )

    download = _save_metadata(
        download,
        metadata_directory
    )

    if stitch:

        download = _stitch_lightcurves(
            download
        )

    return download