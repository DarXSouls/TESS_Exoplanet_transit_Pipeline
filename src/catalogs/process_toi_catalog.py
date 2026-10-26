from pathlib import Path

import pandas as pd

from datetime import datetime


  
# TOI DISPOSITION CLASSES
  

CONFIRMED_CLASSES = [
    "CP",      # Confirmed Planet
    "KP"       # Known Planet
]

FALSE_POSITIVE_CLASSES = [
    "FP",      # False Positive
    "FA"       # False Alarm
]

CANDIDATE_CLASSES = [
    "PC",      # Planet Candidate
    "APC"      # Ambiguous Planet Candidate
]


  
# REQUIRED COLUMNS
  

REQUIRED_COLUMNS = [

    "tid",
    "toi",
    "tfopwg_disp",

    "pl_orbper",
    "pl_trandurh",
    "pl_trandep",

    "st_tmag",

    "ra",
    "dec"
]


  
# COLUMN MAPPING
  

COLUMN_MAPPING = {

    "tid": "TICID",

    "toi": "TOI",

    "pl_orbper": "PERIOD",

    "pl_trandurh": "TRANSIT_DURATION",

    "pl_trandep": "TRANSIT_DEPTH",

    "st_tmag": "TMAG",

    "ra": "RA",

    "dec": "DEC"

}


  
# PROJECT COLUMN ORDER
  

PROJECT_COLUMNS = [

    "TICID",

    "TOI",

    "SOURCE",

    "CATALOG_LABEL",

    "CATALOG_VERSION",

    "CATALOG_PROCESSED_DATE",

    "tfopwg_disp",

    "PERIOD",

    "TRANSIT_DURATION",

    "TRANSIT_DEPTH",

    "TMAG",

    "RA",

    "DEC"

]


  
# VALIDATE CATALOG
  

def validate_catalog(
    dataframe
):
    """
    Validate that all required columns exist.
    """

    missing_columns = [

        column

        for column in REQUIRED_COLUMNS

        if column not in dataframe.columns

    ]

    if len(missing_columns):

        raise ValueError(

            f"Missing required columns: {missing_columns}"

        )


  
# REMOVE DUPLICATE TIC IDs
  

def remove_duplicates(
    dataframe
):
    """
    Remove duplicate TIC IDs.
    """

    return dataframe.drop_duplicates(
        subset="tid"
    )


  
# STANDARDIZE COLUMN NAMES
  

def standardize_columns(
    dataframe
):
    """
    Rename TOI catalog columns to project standard.
    """

    return dataframe.rename(
        columns=COLUMN_MAPPING
    )


  
# REORDER COLUMNS
  

def reorder_columns(
    dataframe
):
    """
    Move important project columns to the front while
    preserving all remaining columns.
    """

    existing_columns = [

        column

        for column in PROJECT_COLUMNS

        if column in dataframe.columns

    ]

    remaining_columns = [

        column

        for column in dataframe.columns

        if column not in existing_columns

    ]

    return dataframe[
        existing_columns +
        remaining_columns
    ]


  
# FILTER BY DISPOSITION
  

def filter_catalog(
    dataframe,
    dispositions
):
    """
    Filter catalog using TOI disposition classes.
    """

    return dataframe[
        dataframe["tfopwg_disp"].isin(
            dispositions
        )
    ].copy()


  
# SAVE CATALOG
  

def save_catalog(
    dataframe,
    filename,
    output_dir
):
    """
    Save processed catalog.
    """

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = output_dir / filename

    dataframe.to_csv(
        output_file,
        index=False
    )

    print(
        f"Saved: {output_file.name}"
    )


  
# PROCESS TOI CATALOG
  

def process_toi_catalog(
    input_file,
    output_dir,
    catalog_version="2025-06"
):
    """
    Process the raw TOI catalog into:

    - confirmed_planets.csv
    - false_positives.csv
    - planet_candidates.csv
    """

    input_file = Path(input_file)
    output_dir = Path(output_dir)

    print(
        "\nLoading TOI Catalog..."
    )

    df = pd.read_csv(
        input_file
    )

     
    # Validate Catalog
     

    validate_catalog(
        df
    )

     
    # Remove Duplicate TIC IDs
     

    df = remove_duplicates(
        df
    )

     
    # Standardize Column Names
     

    df = standardize_columns(
        df
    )

     
    # Project Standard Columns
     

    df["SOURCE"] = "TOI"

    df["CATALOG_LABEL"] = df["tfopwg_disp"]

    df["CATALOG_VERSION"] = catalog_version

    df["CATALOG_PROCESSED_DATE"] = datetime.now().strftime("%Y-%m-%d")

     
    # Reorder Columns
     

    df = reorder_columns(
        df
    )

     
    # Split Catalog
     

    confirmed = filter_catalog(
        df,
        CONFIRMED_CLASSES
    )

    false_positive = filter_catalog(
        df,
        FALSE_POSITIVE_CLASSES
    )

    candidates = filter_catalog(
        df,
        CANDIDATE_CLASSES
    )

     
    # Save Processed Catalogs
     

    save_catalog(
        confirmed,
        "confirmed_planets.csv",
        output_dir
    )

    save_catalog(
        false_positive,
        "false_positives.csv",
        output_dir
    )

    save_catalog(
        candidates,
        "planet_candidates.csv",
        output_dir
    )

     
    # Summary
     

    print("\n========== TOI Catalog Summary ==========\n")

    print(
        f"Confirmed Planets : {len(confirmed)}"
    )

    print(
        f"False Positives   : {len(false_positive)}"
    )

    print(
        f"Planet Candidates : {len(candidates)}"
    )

    print(
        f"Total Objects     : {len(df)}"
    )

    print(
        "\n=========================================\n"
    )

    return {

        "confirmed_planets": confirmed,

        "false_positives": false_positive,

        "planet_candidates": candidates

    }