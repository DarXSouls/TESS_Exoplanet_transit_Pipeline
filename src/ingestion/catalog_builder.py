import json
import pandas as pd

from pathlib import Path

def build_catalog(
    metadata_dir,
    output_file
):

    rows = []

    metadata_dir = Path(
        metadata_dir
    )

    for file in metadata_dir.glob(
        "*.json"
    ):

        with open(file) as f:

            rows.append(
                json.load(f)
            )

    catalog = pd.DataFrame(
        rows
    )

    catalog.to_csv(
        output_file,
        index=False
    )

    print(
        f"Catalog saved to {output_file}"
    )

    return catalog