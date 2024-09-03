# from io import TextIOWrapper
# import re
# import numpy as np
# import pandas as pd
# from itertools import product
# from random import sample
import os
import requests
from multiprocessing import Pool
# from multiprocess import Pool
import logging
logging.basicConfig(level=logging.INFO)
from tqdm.notebook import tqdm
# import sys
# from io import StringIO



def files_download(file_data:list[tuple]) -> str:
    _, file = file_data[0]
    path_dir = os.path.dirname(file)
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
    res=[]
    with Pool() as p:
        res = list(tqdm(p.imap(file_preprocess, file_data), total=len(file_data)))
    return res
    
def file_preprocess(file_data) -> str:
    url, file = file_data
    return file_download_path(url, file)

def file_download_path(url_path: str, file_path: str) -> str:
    ### Download file from url_path to file_path
    # It will download the file if it does not exist
    # It will return the file path after download or if it already exists
    if not os.path.exists(file_path):
        # print(f"\033[32mDownloading file ...\033[0m")
        logging.info(f"\033[32mDownloading file ...\033[0m")
        with requests.get(url_path) as response:
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                logging.info(f"Download complete. path: \033[32m{file_path}\033[0m")
                # print(f"Download complete. path: \033[32m{file_path}\033[0m")
            else:
                logging.info(f"Error: {response.status_code}")
                # print(f"Error: {response.status_code}")
    else:
        logging.info("File already exists.")
        # print("File already exists.")
    return file_path