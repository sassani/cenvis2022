import os
import logging
import requests
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