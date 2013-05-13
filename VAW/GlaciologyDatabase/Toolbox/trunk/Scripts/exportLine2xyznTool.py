import arcpy, exportGlacierData.exportPolyline2xyzn

sourceLayer = arcpy.GetParameter(0)
targetFile = arcpy.GetParameterAsText(1)

exportGlacierData.exportPolyline2xyzn.doExport(sourceLayer, targetFile)
