import arcpy, exportGlacierData.exportPolyline2xyzn

sourceLayer = arcpy.GetParameter(0)
targetFile = arcpy.GetParameterAsText(1)
altitudeField = arcpy.GetParameterAsText(2)
pointIdField = arcpy.GetParameterAsText(3)

exportGlacierData.exportPolyline2xyzn.doExport(sourceLayer, targetFile, altitudeField, pointIdField)
