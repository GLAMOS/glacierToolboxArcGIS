# Copyright ETH-VAW / Glaciology
#
# Module     : Scripts.convertPolygonToPolylineTool
# 
# Created by: yvow
# Created on: 06.12.2013

'''
Converts polygons into individual polylines. An individual polyline represents an individual part of the input geometry.
Shared boundaries of polygons are converted as individual polylines.
A polylines starts with vertex 0 and ends with vertex 0 again to close to polyline.
'''

# Imports
import arcpy, convertGlacierData.convertPolygonToPolyline

sourcePolygonLayer = arcpy.GetParameter(0)
targetPolylineLayer = arcpy.GetParameterAsText(1)

convertGlacierData.convertPolygonToPolyline.doConversion(sourcePolygonLayer, targetPolylineLayer)

arcpy.RefreshActiveView()

# Refresh ArcMap with the newly converted data.
arcpy.AddMessage("End of the conversion between polygon and polyline.")