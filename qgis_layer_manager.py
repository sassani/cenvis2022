from qgis.core import QgsVectorLayer, QgsProject, QgsField, QgsFeature
from PyQt5.QtCore import QVariant
import csv
from typing import List, Dict, Any


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
                headers[i]: row[i] 
                for i in range(len(headers)) 
                if headers[i] not in [join_field_variable, 'state','county','tract']  # Skip GIDTR as it's the key
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
                    field = QgsField(header, QVariant.Int)
                elif sample_value.replace('$', '').isdigit():
                    field = QgsField(header, QVariant.Double)
                elif sample_value.replace('.', '').isdigit():
                    field = QgsField(header, QVariant.Double)
                else:
                    field = QgsField(header, QVariant.String)
                    
                layer.addAttribute(field)
                new_fields.append(header)
        print(*layer.getFeatures())
        return True
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

# Example usage
"""
# Assuming you have your layer and data ready:
layer = QgsProject.instance().mapLayersByName('your_layer_name')[0]
data = [
    ["GIDTR", "Age5p_Arabic_ACS_16_20", "state", "county", "tract"],
    ["02013000100", "14", "02", "013", "000100"]
]

success = join_data_to_layer(layer, data)
if success:
    print("Data joined successfully!")
else:
    print("Failed to join data")
"""
