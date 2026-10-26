"""
==========================================================
Download Models
==========================================================

Dataclasses used by the TESS ingestion pipeline.

These classes define the objects exchanged between the
different stages of the download pipeline.

Pipeline
--------
SearchResult
        │
        ▼
ProductSelection
        │
        ▼
DownloadResult
        │
        ▼
DownloadSummary

==========================================================
"""

from dataclasses import dataclass, field
from pathlib import Path
import pandas as pd

from lightkurve.search import SearchResult
from lightkurve.collections import LightCurveCollection
from lightkurve.lightcurve import TessLightCurve


# PRODUCT SELECTION

@dataclass(slots=True, frozen=True)
class ProductSelection:
    """
    Products selected for download.
    """

    tic_id: int

    products: SearchResult

    cadence: int

    sectors: list[int]

    n_products: int

    mission: str

    author: str



# DOWNLOAD RESULT

@dataclass(slots=True)
class DownloadResult:
    """
    Downloaded products.
    """

    selection: ProductSelection

    collection: LightCurveCollection

    fits_files: list[Path] = field(default_factory=list)

    stitched_lightcurve: TessLightCurve | None = None

    dataframe: pd.DataFrame | None = None

    metadata: dict | None = None

    parquet_file: Path | None = None

    metadata_file: Path | None = None





# DOWNLOAD SUMMARY

@dataclass(slots=True)
class DownloadSummary:
    """
    Final download summary returned by
    download_tess_target().
    """

    tic_id: int

    status: str

    pipeline_version: str

    cadence: int

    n_products: int

    n_sectors: int

    fits_files: list[Path]

    parquet_file: Path

    metadata_file: Path