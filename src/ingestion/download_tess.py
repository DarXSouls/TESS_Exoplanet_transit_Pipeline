import json
import shutil

import lightkurve as lk
import numpy as np
import pandas as pd

from pathlib import Path
from astropy.io import fits

from tqdm import tqdm
from datetime import datetime


def download_tess_target(
    tic_id,
    fits_dir,
    parquet_dir,
    metadata_dir,
    mission="TESS",
    author="SPOC"
):
    """
    Download a TESS target and save:

    1. Original FITS file
    2. Extracted parquet file
    3. Metadata JSON

    Parameters
    ----------
    tic_id : int

    fits_dir : Path

    parquet_dir : Path

    metadata_dir : Path
    """

    print(f"Downloading TIC {tic_id}")

    fits_dir = Path(fits_dir)
    parquet_dir = Path(parquet_dir)
    metadata_dir = Path(metadata_dir)

    fits_dir.mkdir(parents=True, exist_ok=True)
    parquet_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)

    search = lk.search_lightcurve(
        f"TIC {tic_id}",
        mission=mission,
        author=author
    )

    if len(search) == 0:
        print(f"No data found for TIC {tic_id}")
        return None

    lc = search[0].download()

    fits_path = Path(lc.filename)

   
    # Save Original FITS

    fits_output = fits_dir / f"TIC_{tic_id}.fits"

    if not fits_output.exists():
        shutil.copy2(
            fits_path,
            fits_output
        )

    
    # Open FITS

    hdul = fits.open(fits_path)

    data = hdul[1].data

    
    # Extract Required Columns

    df = pd.DataFrame({

        "TIME":
            np.array(data["TIME"], dtype=np.float64),

        "SAP_FLUX":
            np.array(data["SAP_FLUX"], dtype=np.float32),

        "SAP_FLUX_ERR":
            np.array(data["SAP_FLUX_ERR"], dtype=np.float32),

        "PDCSAP_FLUX":
            np.array(data["PDCSAP_FLUX"], dtype=np.float32),

        "PDCSAP_FLUX_ERR":
            np.array(data["PDCSAP_FLUX_ERR"], dtype=np.float32),

        "QUALITY":
            np.array(data["QUALITY"], dtype=np.int32),

        "PSF_CENTR1":
            np.array(data["PSF_CENTR1"], dtype=np.float32),

        "PSF_CENTR2":
            np.array(data["PSF_CENTR2"], dtype=np.float32),

        "MOM_CENTR1":
            np.array(data["MOM_CENTR1"], dtype=np.float32),

        "MOM_CENTR2":
            np.array(data["MOM_CENTR2"], dtype=np.float32),
    })


    # Save Parquet

    parquet_file = (
        parquet_dir /
        f"TIC_{tic_id}.parquet"
    )

    df.to_parquet(
        parquet_file,
        index=False
    )

    
    # Metadata

    header = hdul[0].header

    metadata = {

        "TICID":
            header.get("TICID"),

        "SECTOR":
            header.get("SECTOR"),

        "CAMERA":
            header.get("CAMERA"),

        "CCD":
            header.get("CCD"),

        "TMAG":
            header.get("TESSMAG"),

        "RA":
            header.get("RA_OBJ"),

        "DEC":
            header.get("DEC_OBJ")
    }

    metadata_file = (
        metadata_dir /
        f"TIC_{tic_id}.json"
    )

    with open(metadata_file, "w") as f:
        json.dump(
            metadata,
            f,
            indent=4
        )

    hdul.close()

    print(f"Saved TIC {tic_id}")

    return {
        "fits": fits_output,
        "parquet": parquet_file,
        "metadata": metadata_file
    }





# def download_multiple_targets(
#     tic_ids,
#     fits_dir,
#     parquet_dir,
#     metadata_dir,
#     log_file=None
# ):

#     results = []

#     for tic_id in tqdm(
#         tic_ids,
#         desc="Downloading Targets"
#     ):

#         try:

#             output = download_tess_target(
#                 tic_id=tic_id,
#                 fits_dir=fits_dir,
#                 parquet_dir=parquet_dir,
#                 metadata_dir=metadata_dir
#             )

#             results.append({

#                 "TICID": tic_id,
#                 "STATUS": "SUCCESS",
#                 "DATE": datetime.now()
#             })

#         except Exception as e:

#             print(
#                 f"Failed TIC {tic_id}"
#             )

#             results.append({

#                 "TICID": tic_id,
#                 "STATUS": "FAILED",
#                 "DATE": datetime.now(),
#                 "ERROR": str(e)
#             })

#     if log_file is not None:

#         pd.DataFrame(
#             results
#         ).to_csv(
#             log_file,
#             index=False
#         )

#     return pd.DataFrame(results)

