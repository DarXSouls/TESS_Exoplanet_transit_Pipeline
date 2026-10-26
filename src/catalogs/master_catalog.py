"""
==========================================================

Master Catalog Builder

Combines all processed catalogs into a single
master catalog.

Responsibilities

- Merge processed catalogs
- Resolve duplicate TICIDs
- Apply label priority policy
- Initialize pipeline status
- Export master catalog
- Export conflicts
- Generate statistics

==========================================================
"""


from pathlib import Path

import pandas as pd

from utils.project_constants import (

    PRIMARY_KEY,

    CLASS_MAPPING,

    LABEL_PRIORITY,

    INITIAL_PIPELINE_STATUS,

    MASTER_COLUMNS,

    MASTER_BASE_COLUMNS

)
 

# All remaining metadata
# (RA, DEC, PERIOD, TMAG, etc.)
# are identical after catalog standardization,
# therefore we retain the first row and overwrite
# only catalog-level metadata.


 
# LOAD PROCESSED CATALOGS
 

def load_catalogs(
    catalog_directory
):
    """
    Load all processed catalogs.
    """

    catalog_directory = Path(catalog_directory)

    catalogs = {

        "confirmed_planets":

            pd.read_csv(
                catalog_directory /
                "confirmed_planets.csv"
            ),

        "false_positives":

            pd.read_csv(
                catalog_directory /
                "false_positives.csv"
            ),

        "planet_candidates":

            pd.read_csv(
                catalog_directory /
                "planet_candidates.csv"
            ),

        "eclipsing_binaries":

            pd.read_csv(
                catalog_directory /
                "eclipsing_binaries.csv"
            )

    }

    return catalogs


 
# MERGE CATALOGS
 

def merge_catalogs(
    catalogs
):
    """
    Merge all processed catalogs.
    """

    master = pd.concat(

        catalogs.values(),

        ignore_index=True

    )

    master = master.sort_values(

        PRIMARY_KEY

    ).reset_index(

        drop=True

    )

    return master





# RESOLVE PRIMARY LABEL


def resolve_primary_label(
    labels
):
    """
    Resolve the highest-priority catalog label.
    """

    labels = sorted(set(labels))

    return min(

        labels,

        key=lambda label:
        LABEL_PRIORITY[label]

    )





# MERGE VALUES


def merge_values(
    values
):
    """
    Merge unique values into a semicolon-separated string.
    """

    values = sorted({

        str(value)

        for value in values

        if pd.notna(value)

    })

    return ";".join(values)






# Each TICID represents one astrophysical object.

# Multiple catalog entries are collapsed into a
# single master record using the project's label
# priority policy.



# RESOLVE CONFLICTS


def resolve_conflicts(
    master
):
    """
    Resolve duplicate TICIDs and build one
    record per target.
    """

    resolved_rows = []

    for _, group in master.groupby(PRIMARY_KEY):

        base_row = group.iloc[0].copy()

        unique_sources = group["SOURCE"].dropna().unique()

        unique_labels =group[
            "CATALOG_LABEL"
            ].dropna().unique()
        

        base_row["SOURCE"] = merge_values(unique_sources)

        base_row["CATALOG_LABEL"] = merge_values(unique_labels)

        base_row["PRIMARY_LABEL"] = resolve_primary_label(
            unique_labels
        )

        base_row["FINAL_CLASS"] = CLASS_MAPPING[
            base_row["PRIMARY_LABEL"]
        ]

        base_row["IS_CONFLICT"] = len(unique_labels) > 1

        base_row["N_SOURCES"] = len(set(unique_sources))

        base_row["LABEL_STATUS"] = (

            "Conflict"

            if base_row["IS_CONFLICT"]

            else "Clean"

        )

        resolved_rows.append(
            base_row.copy()
            )


    master = pd.DataFrame(
        resolved_rows
    )
    

    remaining_columns = [
        
        column
        
        for column in master.columns
        
        if column not in MASTER_BASE_COLUMNS
        
        ]
    
    master = master[
        MASTER_BASE_COLUMNS + remaining_columns
    ]



    master = master.sort_values(
        PRIMARY_KEY
    ).reset_index(
        drop=True
    )

    return master




def export_conflicts(
    master,
    output_directory
):

    conflicts = master[
        master["IS_CONFLICT"]
    ]

    save_catalog(

        conflicts,

        "conflicts.csv",

        output_directory

    )



def generate_statistics(
    master
):

    print("\n========== Master Catalog ==========\n")


    print(
        f"Planets             : {(master['FINAL_CLASS']=='Planet').sum()}"
    )

    print(
        f"Candidates          : {(master['FINAL_CLASS']=='Candidate').sum()}"
    )

    print(
        f"False Positives     : {(master['FINAL_CLASS']=='False Positive').sum()}"
    )

    print(
        f"Eclipsing Binaries  : {(master['FINAL_CLASS']=='Eclipsing Binary').sum()}"
    )

    print(
        f"Conflicts           : {master['IS_CONFLICT'].sum()}"
    )

    print(
        f"Unique TICIDs       : {len(master)}"
    )

    print()





 
# INITIALIZE PIPELINE STATUS
 

def initialize_pipeline_status(
    dataframe
):
    """
    Add pipeline status columns.
    """

    for column, value in INITIAL_PIPELINE_STATUS.items():

        dataframe[column] = value

    return dataframe


 
# SAVE CATALOG
 

def save_catalog(
    dataframe,
    filename,
    output_directory
):

    output_directory = Path(
        output_directory
    )

    output_directory.mkdir(

        parents=True,

        exist_ok=True

    )

    dataframe.to_csv(

        output_directory / filename,

        index=False

    )

    print(

        f"Saved: {filename}"

    )


 
# CREATE MASTER CATALOG
 

def create_master_catalog(
    processed_catalog_directory,
    output_directory
):

    print(

        "\nLoading Processed Catalogs..."

    )

    catalogs = load_catalogs(

        processed_catalog_directory

    )

    print(

        "Merging Catalogs..."

    )

    master = merge_catalogs(

        catalogs

    )


    print(
    
    "Resolving Catalog Conflicts..."
    
    )


    master = resolve_conflicts(
        master
    )

    if not master[PRIMARY_KEY].is_unique:
        raise ValueError(
            "Master catalog still contains duplicate TICIDs."
            )




    print(
    
    "Initializing Pipeline Status..."
    
    )


    master = initialize_pipeline_status(

        master

    )

    remaining_columns = [
        
        column
        
        for column in master.columns
        
        if column not in MASTER_BASE_COLUMNS
        
        ]
    
    master = master[
        MASTER_BASE_COLUMNS + remaining_columns
    ]

    
    print(
    
    "Saving Master Catalog..."
    
    )

    save_catalog(

        master,

        "master_catalog.csv",

        output_directory

    )

    export_conflicts(
        master,
        output_directory
    )

    generate_statistics(
        master
    )


    print()

    print("=" * 42)

    print(" Master Catalog Created ")

    print("=" * 42)

    print()

    print(

        f"Total Rows : {len(master)}"

    )

    print()

    return master