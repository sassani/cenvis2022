from qgis.core import (QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsGradientColorRamp,
                       QgsProject, QgsSymbol, QgsGraduatedSymbolRenderer)
from qgis.PyQt.QtCore import QVariant

from .qgis_shapefile_manager import import_zipped_shapefile
from .qgis_layer_manager import join_data_to_layer
import zipfile
import json
import os

class CensusDataVisualizer:
    def __init__(self, shapefile_path, json_folder):
        self.shapefile_path = shapefile_path
        self.json_folder = json_folder
        self.layer = None

    def render_base_layer(self):
        # Load shapefile
        self.layer = import_zipped_shapefile(self.shapefile_path, "Census Tracts")
        
        
    def process_demographic_data(self):
        # Load and process demographic data
        for json_file in os.listdir(self.json_folder):
            if json_file.endswith('.json'):
                field_name = json_file[:-5]
                with open(os.path.join(self.json_folder, json_file), 'r') as f:
                    data = json.load(f)
                    success = join_data_to_layer(self.layer, data)
                    if success:
                        print(f"Data joined successfully for {field_name}")
                    else:
                        print(f"Failed to join data for {field_name}")

