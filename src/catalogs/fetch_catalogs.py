# Instead of manually downloading:

# TOI catalog
# EB catalog

# and placing them in the project, the project can download the latest versions automatically.

"""
==========================================================
Fetch Catalogs
==========================================================

Downloads the latest public catalogs required for the
pipeline.

Responsibilities
----------------
- Download TOI catalog
- Download EB catalog
- Save raw CSV files

==========================================================
"""

from pathlib import Path

import pandas as pd


def download_catalog(
    url,
    output_file
):
    """
    Download a catalog from a URL.
    """

    print(f"Downloading {output_file.name}...")

    dataframe = pd.read_csv(url)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    dataframe.to_csv(
        output_file,
        index=False
    )

    print(f"Saved: {output_file.name}")


def fetch_catalogs(
    toi_url,
    eb_url,
    output_directory
):
    """
    Download all required catalogs.
    """

    output_directory = Path(output_directory)

    download_catalog(
        toi_url,
        output_directory / "toi_catalog.csv"
    )

    download_catalog(
        eb_url,
        output_directory / "eb_catalog.csv"
    )

    print()

    print("=" * 42)
    print(" Catalog Download Complete ")
    print("=" * 42)