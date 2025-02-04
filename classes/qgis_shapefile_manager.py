# from qgis.core import QgsVectorLayer, QgsProject
from zipfile import ZipFile
import os
# import tempfile

def import_zipped_shapefile(zip_path, layer_name=None, counties=None):
    """
    Import a zipped shapefile into QGIS without extracting to a temporary directory.
    
    Args:
        zip_path (str): Path to the zip file containing the shapefile
        layer_name (str, optional): Name to give the layer in QGIS. 
                                  If None, uses the shapefile name
    
    Returns:
        QgsVectorLayer: The loaded vector layer if successful, None otherwise
    """
    try:
        # Create path for zip file
        vsizip_path = f"/vsizip/{zip_path}"
        
        # Find the .shp file in the zip
        with ZipFile(zip_path, 'r') as zip_ref:
            shp_file = next((f for f in zip_ref.namelist() if f.lower().endswith('.shp')), None)
            
        if not shp_file:
            raise ValueError("No shapefile (.shp) found in the zip file")
            
        # Construct full path to shapefile within zip
        full_path = f"{vsizip_path}/{shp_file}"
        
        # Create the vector layer
        if not layer_name:
            layer_name = os.path.splitext(os.path.basename(shp_file))[0]
            
        return full_path, layer_name
            
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
