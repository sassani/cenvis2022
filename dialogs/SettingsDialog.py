from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import QDir
import os
import json
import webbrowser

from ..config.config_manager import ConfigurationManager


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FORM_CLASS_SETTINGS, _ = uic.loadUiType(os.path.join(CURRENT_DIR, "ui/settings.ui"))


class SettingsDialog(QtWidgets.QDialog, FORM_CLASS_SETTINGS):
    def __init__(self, parent=None, config_mng: ConfigurationManager = None):
        super(SettingsDialog, self).__init__(parent)
        self.config_mng: ConfigurationManager = config_mng
        self.setupUi(self)

        self.clbApi.clicked.connect(self.onApiKey)
        self.btnSetDataPath.clicked.connect(self.onBrowsDirectoryDialog)
        self.btnSave.clicked.connect(self.onSaveSettings)
        self.btnCancel.clicked.connect(self.reject)

        self.txtApiKey.setText(config_mng.settings.census_api_key)
        self.txtDataPath.setText(config_mng.settings.data_path)

    def onSaveSettings(self):
        configs = {
            "census_api_key": self.txtApiKey.text(),
            "data_path": self.txtDataPath.text(),
        }
        self.config_mng.save_config(configs)
        self.accept()

    def onApiKey(self):
        webbrowser.open("https://api.census.gov/data/key_signup.html")
        print(self.clbApi.isChecked())

    def onBrowsDirectoryDialog(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Directory", QDir.homePath()
        )
        if directory:  # If a directory was selected (not cancelled)
            self.txtDataPath.setText(directory)
            self.selected_path = directory
