from qgis.core import (
    QgsVectorLayer,
    QgsField,
    QgsFeature,
    QgsGeometry,
    QgsGradientColorRamp,
    QgsProject,
    QgsSymbol,
    QgsGraduatedSymbolRenderer,
)
from qgis.PyQt.QtCore import QVariant

from .data import read_zipped_shapefile, read_json_data

# from .qgis_shapefile_manager import import_zipped_shapefile
from .qgis_layer_manager import (
    join_data_to_layer,
    generate_qgis_layer,
    join_dataframe_to_layer,
)
import zipfile
import json
import os


class CensusDataVisualizer:
    def __init__(self, shapefile_path, json_folder):
        self.shapefile_path = shapefile_path
        self.json_folder = json_folder
        self.base_layer = None

    def generate_base_layer(
        self, layer_name=None, counties_fips: list[str] | None = None
    ):
        shape_path, file_name = read_zipped_shapefile(self.shapefile_path)
        self.base_layer = generate_qgis_layer(
            shape_path,
            layer_name if layer_name else file_name,
            counties_fips=counties_fips,
        )
        # Add the layer to the QGIS project
        self.base_layer.setOpacity(0.5)
        QgsProject.instance().addMapLayer(self.base_layer)

    # def render_base_layer(self):
    #     # Load shapefile
    #     self.layer = read_zipped_shapefile(self.shapefile_path, "Census Tracts")

    def process_demographic_data(self):
        # Load and process demographic data
        for json_file in os.listdir(self.json_folder):
            if json_file.endswith(".json"):
                field_name = json_file[:-5]
                data_path = os.path.join(self.json_folder, json_file)
                df = read_json_data(data_path)
                print(df)
                # with open(os.path.join(self.json_folder, json_file), 'r') as f:
                #     data = json.load(f)
                success = join_dataframe_to_layer(self.base_layer, df)
                if success:
                    print(f"Data joined successfully for {field_name}")
                else:
                    print(f"Failed to join data for {field_name}")
