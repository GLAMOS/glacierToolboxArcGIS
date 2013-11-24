# Copyright 2013 GeoIdee, Sandstrasse 2, CH-8003 Zurich
#
# Module     : Scripts.setVertexAltitudeFromAttributeTool
# 
# Created by: yvow
# Created on: 04.11.2013

'''
Starts the tool to set the z-coordinates of all vertex of a feature to the same value derived from a given attribute.
'''

# Imports
import arcpy, maintenanceGlacierData.setVertexAltitudeFromAttribute

# Layer to be updated
targetLayer = arcpy.GetParameter(0)
# Filed which contains the altitude information.
targetField = arcpy.GetParameter(1)

maintenanceGlacierData.setVertexAltitudeFromAttribute.doVertexUpdate(targetLayer, targetField)