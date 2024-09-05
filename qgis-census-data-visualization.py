from qgis.core import (QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, 
                       QgsProject, QgsSymbol, QgsGraduatedSymbolRenderer)
from qgis.PyQt.QtCore import QVariant
import json
import os

class CensusDataVisualizer:
    def __init__(self, shapefile_path, json_folder):
        self.shapefile_path = shapefile_path
        self.json_folder = json_folder
        self.layer = None

    def load_and_process_data(self):
        # Load shapefile
        self.layer = QgsVectorLayer(self.shapefile_path, "Census Tracts", "ogr")
        if not self.layer.isValid():
            print("Layer failed to load!")
            return

        # Add fields for census data
        self.layer.startEditing()
        for json_file in os.listdir(self.json_folder):
            if json_file.endswith('.json'):
                field_name = json_file[:-5]  # Remove .json extension
                self.layer.addAttribute(QgsField(field_name, QVariant.Double))

        # Populate fields with census data
        for feature in self.layer.getFeatures():
            tract_id = feature['GEOID']  # Assuming GEOID is the tract identifier
            for json_file in os.listdir(self.json_folder):
                if json_file.endswith('.json'):
                    field_name = json_file[:-5]
                    with open(os.path.join(self.json_folder, json_file), 'r') as f:
                        data = json.load(f)
                        value = data.get(tract_id, 0)  # Default to 0 if not found
                        feature[field_name] = value
            self.layer.updateFeature(feature)

        self.layer.commitChanges()

    def display_in_qgis(self, field_to_display):
        if not self.layer:
            print("Layer not loaded!")
            return

        # Create a graduated renderer
        renderer = QgsGraduatedSymbolRenderer()
        renderer.setClassAttribute(field_to_display)

        # Create a color ramp
        color_ramp = QgsGradientColorRamp.create({'color1': '255,255,255,255', 'color2': '255,0,0,255'})

        # Classify the data
        renderer.updateColorRamp(color_ramp)
        renderer.updateClasses(self.layer, QgsGraduatedSymbolRenderer.EqualInterval, 5)

        # Apply the renderer to the layer
        self.layer.setRenderer(renderer)

        # Add layer to the project
        QgsProject.instance().addMapLayer(self.layer)

    def create_web_map(self, output_file):
        # This is a placeholder for web map creation
        # You might use a library like folium or qgis2web for this
        print(f"Web map would be created and saved to {output_file}")
        # Implementation depends on the specific requirements and tools you want to use

# Usage in your QGIS plugin
class YourPlugin:
    def __init__(self, iface):
        self.iface = iface

    def run(self):
        shapefile_path = "/path/to/your/shapefile.shp"
        json_folder = "/path/to/your/json/files/"
        
        visualizer = CensusDataVisualizer(shapefile_path, json_folder)
        visualizer.load_and_process_data()
        visualizer.display_in_qgis("FieldNameToDisplay")
        # visualizer.create_web_map("/path/to/output/webmap.html")

        self.iface.mapCanvas().refresh()
