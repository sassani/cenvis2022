import os
import logging
import requests
from zipfile import ZipFile
import json
import pandas as pd


# from concurrent.futures import ProcessPoolExecutor, as_completed
# from typing import List, Tuple, Callable

# def files_download(file_data: List[Tuple[str, str]], progress_callback: Callable[[int, int], None]) -> List[str]:
#     if file_data:
#         _, file = file_data[0]
#         path_dir = os.path.dirname(file)
#         if not os.path.exists(path_dir):
#             os.makedirs(path_dir)

#     results = []
#     with ProcessPoolExecutor() as executor:
#         future_to_url = {executor.submit(file_download_path, url, file): (url, file) for url, file in file_data}
#         for i, future in enumerate(as_completed(future_to_url), 1):
#             results.append(future.result())
#             progress_callback(i, len(file_data))

#     return results


def file_download_path(url_path: str, file_path: str) -> str:
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        logging.info(f"\033[32mDownloading file ...\033[0m")
        with requests.get(url_path) as response:
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                logging.info(f"Download complete. path: \033[32m{file_path}\033[0m")
            else:
                logging.error(f"Error: {response.status_code}")
    else:
        logging.info("File already exists.")
    return file_path


def read_zipped_shapefile(zip_path):
    """
    Read a zipped shapefile and return the full path to the shapefile within the zip.
    it also returns the name of the shapefile without extension.
    It only returns the full path and the name of the shapefile without extension not any layer data or shapefile data.

    Args:
        zip_path (str): Path to the zip file containing the shapefile
        layer_name (str, optional): Name to give the layer in QGIS.
                                  If None, uses the shapefile name

    Returns:
        full_path (str): The full path to the shapefile within the zip
        file_name (str): The name of the shapefile without extension
    """
    try:
        # Create path for zip file
        vsizip_path = f"/vsizip/{zip_path}"

        # Find the .shp file in the zip
        with ZipFile(zip_path, "r") as zip_ref:
            shp_file = next(
                (f for f in zip_ref.namelist() if f.lower().endswith(".shp")), None
            )

        if not shp_file:
            raise ValueError("No shapefile (.shp) found in the zip file")

        # Construct full path to shapefile within zip
        full_path = f"{vsizip_path}/{shp_file}"

        file_name = os.path.splitext(os.path.basename(shp_file))[0]

        return full_path, file_name

        # layer = QgsVectorLayer(full_path, layer_name, "ogr")

        # # Check if layer is valid
        # if not layer.isValid():
        #     raise ValueError("Layer failed to load!")

        # # Add the layer to the QGIS project
        # QgsProject.instance().addMapLayer(layer)

        # return layer

    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def read_json_data(json_path):
    """
    Read a json file and return the data as a pandas DataFrame.    
    Args:
        json_path (str): Path to the json file        
    Returns:
        pd.DataFrame: Data in the format of a pandas DataFrame
    """
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
            headers = data[0]
            if 'GIDTR' not in headers:
                raise ValueError("GIDTR not found in the JSON headers")
            values = data[1:]
            df = pd.DataFrame(values, columns=headers)
            
            # df = df.set_index('GIDTR')
            # Remove columns 'state', 'county', 'tract' if they exist
            columns_to_remove = ['state', 'county', 'tract']
            df = df.drop(columns=[col for col in columns_to_remove if col in df.columns])
            # Convert columns with $ or . to numeric
            for col in df.columns:
                df[col] = pd.to_numeric(df[col].replace({'\$': '', ',': ''}, regex=True), errors='coerce')
            return df
    except Exception as e:
        print(f"Error: {str(e)}")
        return None