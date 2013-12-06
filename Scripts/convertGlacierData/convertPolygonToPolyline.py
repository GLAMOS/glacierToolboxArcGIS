# Copyright ETH-VAW / Glaciology
#
# Module     : Scripts.convertGlacierData.convertPolygonToPolyline
# 
# Created by: yvow
# Created on: 06.12.2013
from matplotlib.hatch import VerticalHatch

'''
Converts polygons into individual polylines. An individual polyline represents an individual part of the input geometry.
Shared boundaries of polygons are converted as individual polylines.
A polylines starts with vertex 0 and ends with vertex 0 again to close to polyline.
'''

# Imports
import arcpy, os

def doConversion(sourcePolygonLayer, targetPolylineLayer):
    
    dsc = arcpy.Describe(sourcePolygonLayer)
    shapeFieldName = dsc.ShapeFieldName

    arcpy.AddMessage("Shape field name: " + shapeFieldName)

    featureNumber = 0
    searchRows = arcpy.SearchCursor(sourcePolygonLayer)
    
    #featureList = []
    
    insertCursor = arcpy.InsertCursor(targetPolylineLayer, ["SHAPE@"])

    for searchRow in searchRows:
        shapeObj = searchRow.getValue(shapeFieldName)
        
        for partObj in shapeObj:
                
            arcpy.AddMessage("A new part within the current geometry was found.")
            featureNumber = featureNumber + 1
            
            vertexNumber = 0
            
            arrayPolylineVertex = arcpy.Array()
                
            for pointObj in partObj:
                # Handling only valid geometries.
                if (pointObj != None):
                    
                    vertexNumber = vertexNumber + 1
                        
                    arcpy.AddMessage(str(featureNumber) + "." + str(vertexNumber) + " -> " + "X: " + str(pointObj.X) + ", Y: " + str(pointObj.Y) + ", Z: " + str(pointObj.Y))
                    
                    pointVertex = arcpy.Point(pointObj.X, pointObj.Y, pointObj.Z)
                    
                    arrayPolylineVertex.add(pointVertex)
                    
                else:
                    
                    polyline = arcpy.Polyline(arrayPolylineVertex)
                    
                    newPolyline = insertCursor.newRow()
                    newPolyline.setValue("Shape", polyline)
                    insertCursor.insertRow(newPolyline)

                    
                    arcpy.AddMessage("A new part within the current geometry was found.")
                    featureNumber = featureNumber + 1
                    vertexNumber = 0
                    
                    arrayPolylineVertex.removeAll()
                    
            polyline = arcpy.Polyline(arrayPolylineVertex)
                    
            newPolyline = insertCursor.newRow()
            newPolyline.setValue("Shape", polyline)
            insertCursor.insertRow(newPolyline)
                    
    
    #arcpy.CopyFeatures_management(featureList, r"D:\temp\TestPolyline3.shp")

                        