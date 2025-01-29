import os
import sys
from qgis.core import QgsApplication, Qgis

def check_paths():
    print("Current working directory:", os.getcwd())
    print("\nQGIS_PREFIX_PATH:", os.environ.get('QGIS_PREFIX_PATH'))
    print("\nQT_PLUGIN_PATH:", os.environ.get('QT_PLUGIN_PATH'))

print("=== Checking paths before QGIS import ===")
check_paths()

print("\n=== Attempting to import and initialize QGIS ===")
try:
    # Initialize QGIS Application
    qgs = QgsApplication([], False)
    print(f"\nQGIS prefix path: {qgs.prefixPath()}")
    qgs.initQgis()
    
    print("\nQGIS initialized successfully!")
    
    # Try different ways to get version info
    print("QGIS Version (from Qgis class):", Qgis.QGIS_VERSION)
    print("QGIS Version Number:", Qgis.QGIS_VERSION_INT)
    
    # Print loaded libraries
    print("\nLoaded QGIS libraries:")
    for key in dir(qgs):
        if not key.startswith('_'):  # Skip private attributes
            print(f"  {key}")
            
except Exception as e:
    print("\nError:", str(e))
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()

finally:
    try:
        qgs.exitQgis()
        print("\nQGIS cleanup successful")
    except:
        pass