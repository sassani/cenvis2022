from qgis.core import QgsVectorLayer, QgsProject, QgsField, QgsFeature
from PyQt5.QtCore import QVariant
import csv
from typing import List, Dict, Any
import pandas as pd

def generate_qgis_layer(full_path, layer_name, counties_fips: List[str] = None):
    """
    Generate a QGIS vector layer with specified fields, features, and geometry type.
    
    Args:
        full_path (str): Full path to the shapefile
        layer_name (str): Name to give the layer in QGIS
    
    Returns:
        QgsVectorLayer: The generated vector layer if successful, None otherwise
    """
    
    try:
        # Create memory layer
        layer = QgsVectorLayer(full_path, layer_name, "ogr")
        if counties_fips:
            # Create a new layer with only the features that match the counties_fips
            # layer = QgsVectorLayer(full_path, layer_name, "ogr")
            county_field_index = layer.fields().indexOf('COUNTYFP')
            if county_field_index == -1:
                raise ValueError("Field 'COUNTYFP' not found in layer")

            # Select features matching the counties_fips
            layer.selectByExpression(f"\"COUNTYFP\" IN ({','.join(counties_fips)})")
            
            # Create a new memory layer with only selected features
            selected_features = layer.selectedFeatures()
            
            # Create a new memory layer
            memory_layer = QgsVectorLayer(f"Polygon?crs={layer.crs().authid()}", layer_name, "memory")
            memory_provider = memory_layer.dataProvider()
            
            # Add fields from the original layer
            memory_provider.addAttributes(layer.fields())
            memory_layer.updateFields()
            
            # Add only the selected features to the new layer
            memory_provider.addFeatures(selected_features)
            
            return memory_layer
        
        # Check if layer is valid
        if not layer.isValid():
            raise ValueError("Layer failed to load!")
        
        return layer
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def join_data_to_layer(layer: QgsVectorLayer, data: List[List[str]], join_field_base: str = 'GEOID', join_field_variable: str = 'GIDTR') -> bool:
    """
    Join external data to a QGIS vector layer using GIDTR to match with GEOID.
    
    Args:
        layer: QgsVectorLayer - The base vector layer
        data: List[List[str]] - Data in the format [[headers], [values], ...]
        join_field: str - Name of the field in the layer to join on (default: 'GEOID')

    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate inputs
        if len(data) < 2:
            raise ValueError("Data must contain at least headers and one row")
            
        headers = data[0]
        if join_field_variable not in headers:
            raise ValueError(f"Data must contain {join_field_variable} column")
            
        # Create a dictionary from input data
        data_dict = {}
        gidtr_index = headers.index(join_field_variable)
        
        # Process each row of data
        for row in data[1:]:
            if len(row) != len(headers):
                print(f"Warning: Skipping row with incorrect length: {row}")
                continue
            data_dict[row[gidtr_index]] = {
                headers[i]: row[i] for i in range(len(headers)) if headers[i] not in [join_field_variable, 'state','county','tract']  # Skip GIDTR as it's the key
                # if i != gidtr_index  # Skip GIDTR as it's the key
            }
        # print(data_dict)
        # return True
        
        # Start editing the layer
        layer.startEditing()
        
        # Add new fields to the layer
        new_fields = []
        for header in headers:
            if header not in[join_field_variable, 'state','county','tract']:  # keep the variables you want to join
                # Determine field type (try to convert to number if possible)
                sample_value = next(iter(data_dict.values()))[header] if data_dict else ''
                if sample_value.isdigit():
                    field = QgsField(header, QVariant.Double)
                elif sample_value.replace('$', '').isdigit():
                    field = QgsField(header, QVariant.Double)
                elif sample_value.replace('.', '').isdigit():
                    field = QgsField(header, QVariant.Double)
                else:
                    field = QgsField(header, QVariant.String)
                    
                layer.addAttribute(field)
                new_fields.append(header)
        # print(*layer.getFeatures())
        # return True
        # Update layer fields
        layer.updateFields()
        
        # Get field indices
        field_indices = {field: layer.fields().indexOf(field) for field in new_fields}
        geoid_idx = layer.fields().indexOf(join_field_base)
        
        if geoid_idx == -1:
            raise ValueError(f"Join field '{join_field_base}' not found in layer")
            
        # Update features
        matched_count = 0
        total_features = layer.featureCount()
        
        for feature in layer.getFeatures():
            geoid = feature[geoid_idx]
            if geoid in data_dict:
                matched_count += 1
                attrs = {}
                for field, value in data_dict[geoid].items():
                    if field in field_indices:
                        # Convert value to appropriate type
                        if value.isdigit():
                            value = int(value)
                        elif value.replace('.', '').isdigit():
                            value = float(value)
                        attrs[field_indices[field]] = value
                
                layer.changeAttributeValues(feature.id(), attrs)
        
        # Commit changes
        success = layer.commitChanges()
        
        # Print summary
        print(f"Join Summary:")
        print(f"Total features in layer: {total_features}")
        print(f"Matched features: {matched_count}")
        print(f"Unmatched features: {total_features - matched_count}")
        
        return success
        
    except Exception as e:
        print(f"Error joining data: {str(e)}")
        layer.rollBack()
        return False

def join_dataframe_to_layer(layer: QgsVectorLayer, dataframe: pd.DataFrame, join_field_base: str = 'GEOID', join_field_variable: str = 'GIDTR') -> bool:
    """
    Join a pandas DataFrame to a QGIS vector layer using GIDTR to match with GEOID.
    
    Args:
        layer: QgsVectorLayer - The base vector layer
        dataframe: pd.DataFrame - DataFrame containing the data to join
        join_field_base: str - Name of the field in the layer to join on (default: 'GEOID')
        join_field_variable: str - Name of the field in the DataFrame to join on (default: 'GIDTR')
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate inputs
        if dataframe.empty:
            raise ValueError("DataFrame is empty")
        
        if join_field_variable not in dataframe.columns:
            raise ValueError(f"DataFrame must contain {join_field_variable} column")
        
        # Create a dictionary from DataFrame
        data_dict = dataframe.set_index(join_field_variable).to_dict('index')
        # Start editing the layer
        layer.startEditing()
        
        # Add new fields to the layer
        new_fields = []
        for column in dataframe.columns:
            if column != join_field_variable:
                sample_value = dataframe[column].iloc[0]
                if pd.api.types.is_numeric_dtype(dataframe[column]):
                    field = QgsField(column, QVariant.Double)
                else:
                    field = QgsField(column, QVariant.String)
                    
                layer.addAttribute(field)
                new_fields.append(column)
        
        # Update layer fields
        layer.updateFields()
        
        # Get field indices
        field_indices = {field: layer.fields().indexOf(field) for field in new_fields}
        geoid_idx = layer.fields().indexOf(join_field_base)
        
        if geoid_idx == -1:
            raise ValueError(f"Join field '{join_field_base}' not found in layer")
            
        # Update features
        matched_count = 0
        total_features = layer.featureCount()
        
        for feature in layer.getFeatures():
            geoid = feature[geoid_idx]
            if geoid in data_dict:
                matched_count += 1
                attrs = {}
                for field, value in data_dict[geoid].items():
                    if field in field_indices:
                        attrs[field_indices[field]] = value
                
                layer.changeAttributeValues(feature.id(), attrs)
        
        # Commit changes
        success = layer.commitChanges()
        
        # Print summary
        print(f"Join Summary:")
        print(f"Total features in layer: {total_features}")
        print(f"Matched features: {matched_count}")
        print(f"Unmatched features: {total_features - matched_count}")
        
        return success
        
    except Exception as e:
        print(f"Error joining data: {str(e)}")
        layer.rollBack()
        return False