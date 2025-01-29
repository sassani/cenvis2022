import os
import sys
from ctypes import WinDLL
import platform

def print_system_info():
    print(f"Python Version: {sys.version}")
    print(f"Architecture: {platform.architecture()}")
    print(f"Python Path: {sys.executable}")
    print("\nPYTHONPATH:")
    for path in sys.path:
        print(f"  {path}")

def find_dll(dll_name):
    paths = os.environ['PATH'].split(';')
    found_paths = []
    for path in paths:
        dll_path = os.path.join(path, dll_name)
        if os.path.exists(dll_path):
            found_paths.append(dll_path)
    return found_paths

def try_load_dll(dll_path):
    try:
        WinDLL(dll_path)
        return True, None
    except Exception as e:
        return False, str(e)

# Print system information
print("=== System Information ===")
print_system_info()

# Check QGIS environment variables
print("\n=== QGIS Environment Variables ===")
qgis_vars = ['QGIS_PREFIX_PATH', 'PYTHONPATH', 'QT_PLUGIN_PATH', 'PATH']
for var in qgis_vars:
    print(f"{var}: {os.environ.get(var, 'Not set')}")

# Look for qgis_core.dll
print("\n=== Searching for qgis_core.dll ===")
found_paths = find_dll('qgis_core.dll')
if found_paths:
    print("Found qgis_core.dll in:")
    for path in found_paths:
        print(f"  {path}")
        success, error = try_load_dll(path)
        print(f"  Load attempt: {'Success' if success else f'Failed - {error}'}")
else:
    print("qgis_core.dll not found in PATH")

# Look for key dependencies
print("\n=== Checking Qt Dependencies ===")
qt_dlls = ['Qt5Core.dll', 'Qt5Gui.dll', 'Qt5Widgets.dll']
for dll in qt_dlls:
    paths = find_dll(dll)
    if paths:
        print(f"\nFound {dll} in:")
        for path in paths:
            print(f"  {path}")
    else:
        print(f"\n{dll} not found in PATH")