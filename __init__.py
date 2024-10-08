# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CenVis2022
                                 A QGIS plugin
 Download the US cencus data for 2022
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-09-03
        copyright            : (C) 2024 by Ardavan Sassani
        email                : a.sassani@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load CenVis2022 class from file CenVis2022.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .CenVis2022 import CenVis2022
    return CenVis2022(iface)
