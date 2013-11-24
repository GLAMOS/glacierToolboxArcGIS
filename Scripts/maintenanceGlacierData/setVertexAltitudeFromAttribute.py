# Copyright ETH-VAW / Glaciology
#
# Module     : Scripts.maintenanceGlacierData.setVertexAltitudeFromAttribute
# 
# Created by: yvow
# Created on: 04.11.2013

'''
Sets the z coordinates of all individual vertex of a feature to the value in a given attribute.
This functionality can be used to set the z-values within contour lines without the very complicate 
way to do it with the build-in functionality of ArcGIS.
'''

# Imports
import arcpy

def doVertexUpdate(targetLayer, altitudeField):
    
    dsc = arcpy.Describe(targetLayer)
    shapeFieldName = dsc.ShapeFieldName

    arcpy.AddMessage("Shape field name: " + shapeFieldName)

    updateRows = arcpy.UpdateCursor(targetLayer)

    for updateRow in updateRows:
        shapeObj = updateRow.getValue(shapeFieldName)
        altitude = updateRow.getValue(altitudeField)
        
        arcpy.AddMessage("The altitude of a geometry will be set.")
        
        geomArr = arcpy.Array()
         
        # Loop for MultiPart
        for partObj in shapeObj:
            
            partArr = arcpy.Array()
            
            for pointObj in partObj:
                # Handling only valid geometries.
                if (pointObj != None):
                                        
                    pntOut = arcpy.Point(pointObj.X, pointObj.Y, altitude)
                    partArr.add(pntOut)
                    
                geomArr.add(partArr)
        
        polyline = arcpy.Polyline(geomArr)
        
        updateRow.setValue(shapeFieldName, polyline)
        updateRows.updateRow(updateRow)
    
        del updateRow
                    
    del updateRows
    