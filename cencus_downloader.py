from qgis.PyQt.QtCore import QObject, pyqtSignal
# from PyQt5.QtCore import QObject, pyqtSignal
import os
import requests
import json

from .data import file_download_path

class CensusDownloader(QObject):
    progress = pyqtSignal(int, int)
    finished = pyqtSignal(list)

    def __init__(self, census_data):
        super().__init__()
        self.census_data = census_data

    def run(self):
        results = []
        for i, (url, file_path) in enumerate(self.census_data, 1):
            result = file_download_path(url, file_path)
            # result = self._download_census_data(url, file_path)
            results.append(result)
            self.progress.emit(i, len(self.census_data))
        self.finished.emit(results)

    def _download_census_data(self, url, file_path):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                return file_path
            else:
                return f"Error: HTTP {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"