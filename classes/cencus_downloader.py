from qgis.PyQt.QtCore import QObject, pyqtSignal
# from PyQt5.QtCore import QObject, pyqtSignal
import os
import requests
import json

from .file_manager import file_download_path

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