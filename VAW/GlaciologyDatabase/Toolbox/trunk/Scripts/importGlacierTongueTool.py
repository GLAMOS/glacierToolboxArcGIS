import arcpy, importGlacierData.importTongue

targetLayer = arcpy.GetParameter(0)
sourceLayer = arcpy.GetParameter(1)
glacierId = arcpy.GetParameterAsText(2)
measureDate = arcpy.GetParameter(3)

arcpy.AddMessage("Start to import the glacier tongue ...")

importGlacierData.importTongue.doImport(targetLayer, sourceLayer, glacierId, measureDate)

arcpy.RefreshActiveView()

# Refresh the ArcMap frontend with the newly added data.
arcpy.AddMessage("End of the import of the glacier tongue.")
# TODO: The open attribute table of the glacier tongue will not be updated. So far no solution by ArcPy found.
