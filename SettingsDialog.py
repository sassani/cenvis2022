from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import QDir
import os
import json
import webbrowser


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FORM_CLASS_SETTINGS, _ = uic.loadUiType(os.path.join(CURRENT_DIR, 'settings.ui'))

class SettingsDialog(QtWidgets.QDialog, FORM_CLASS_SETTINGS):
    def __init__(self, parent=None, _settings=None):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)

        self.clbApi.clicked.connect(self.api_clicked)
        self.btnSetDataPath.clicked.connect(self.open_directory_dialog)
        self.btnSave.clicked.connect(self.save_settings)
        self.btnCancel.clicked.connect(self.reject)

        self.txtApiKey.setText(_settings['census_api_key'])
        self.txtDataPath.setText(_settings['data_path'])

    def save_settings(self):
        _settings={}
        _settings['census_api_key'] = self.txtApiKey.text()
        _settings['data_path'] = self.txtDataPath.text()
        with open(os.path.join(CURRENT_DIR, 'settings.json'), 'w') as f:
            json.dump(_settings, f)
        self.accept()


    def api_clicked(self):
        webbrowser.open('https://api.census.gov/data/key_signup.html')
        print(self.clbApi.isChecked())

    def open_directory_dialog(self):
        # Open the directory selection dialog
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", QDir.homePath())
        if directory:  # If a directory was selected (not cancelled)
            self.txtDataPath.setText(directory)
            self.selected_path = directory