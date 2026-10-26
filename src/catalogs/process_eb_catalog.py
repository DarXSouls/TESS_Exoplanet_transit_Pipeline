from pathlib import Path
from datetime import datetime

import pandas as pd


  
# REQUIRED COLUMNS
  

REQUIRED_COLUMNS = [

    "tess_id",

    "period",

    "Tmag",

    "ra",

    "dec",

    "morph_coeff",

    "prim_depth_pf",

    "sec_depth_pf"

]


  
# COLUMN MAPPING
  

COLUMN_MAPPING = {

    "tess_id": "TICID",

    "period": "PERIOD",

    "Tmag": "TMAG",

    "ra": "RA",

    "dec": "DEC",

    "morph_coeff": "MORPH_COEFF",

    "prim_depth_pf": "PRIMARY_DEPTH",

    "sec_depth_pf": "SECONDARY_DEPTH",

    "bjd0": "EPOCH",

    "sectors": "SECTORS"

}


  
# PROJECT COLUMN ORDER
  

PROJECT_COLUMNS = [

    "TICID",

    "SOURCE",

    "CATALOG_LABEL",

    "CATALOG_VERSION",

    "CATALOG_PROCESSED_DATE",

    "PERIOD",

    "EPOCH",

    "TMAG",

    "RA",

    "DEC",

    "MORPH_COEFF",

    "PRIMARY_DEPTH",

    "SECONDARY_DEPTH",

    "SECTORS"

]


  
# VALIDATE CATALOG
  

def validate_catalog(
    dataframe
):

    missing_columns = [

        column

        for column in REQUIRED_COLUMNS

        if column not in dataframe.columns

    ]

    if len(missing_columns):

        raise ValueError(

            f"Missing required columns: {missing_columns}"

        )


  
# REMOVE DUPLICATES
  

def remove_duplicates(
    dataframe
):

    return dataframe.drop_duplicates(
        subset="tess_id"
    )


  
# STANDARDIZE COLUMN NAMES
  

def standardize_columns(
    dataframe
):

    return dataframe.rename(
        columns=COLUMN_MAPPING
    )


  
# REORDER COLUMNS
  

def reorder_columns(
    dataframe
):

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


  
# SAVE CATALOG
  

def save_catalog(
    dataframe,
    filename,
    output_dir
):

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


  
# PROCESS EB CATALOG
  

def process_eb_catalog(
    input_file,
    output_dir,
    catalog_version="2025-06"
):

    input_file = Path(input_file)
    output_dir = Path(output_dir)

    print(
        "\nLoading EB Catalog..."
    )

    df = pd.read_csv(
        input_file
    )

      
    # Validate
      

    validate_catalog(
        df
    )

      
    # Remove Duplicates
      

    df = remove_duplicates(
        df
    )

      
    # Standardize Columns
      

    df = standardize_columns(
        df
    )

      
    # Project Columns
      

    df["SOURCE"] = "EB"

    df["CATALOG_LABEL"] = "EB"

    df["CATALOG_VERSION"] = catalog_version

    df["CATALOG_PROCESSED_DATE"] = datetime.now().strftime("%Y-%m-%d")

      
    # Reorder Columns
      

    df = reorder_columns(
        df
    )

      
    # Save
      

    save_catalog(
        df,
        "eclipsing_binaries.csv",
        output_dir
    )

      
    # Summary
      

    print("\n========== EB Catalog Summary ==========\n")

    print(
        f"Eclipsing Binaries : {len(df)}"
    )

    print(
        "\n========================================\n"
    )

    return {

        "eclipsing_binaries": df

    }