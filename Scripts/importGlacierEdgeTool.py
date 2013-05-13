import arcpy, importGlacierData.importEdge

targetLayer = arcpy.GetParameter(0)
sourceLayer = arcpy.GetParameter(1)
glacierId = arcpy.GetParameterAsText(2)
measureDate = arcpy.GetParameter(3)
subName = arcpy.GetParameterAsText(4)

arcpy.AddMessage("Start to import the glacier edge ...")

importGlacierData.importEdge.doImport(targetLayer, sourceLayer, glacierId, measureDate, subName)

arcpy.RefreshActiveView()

# Refresh the ArcMap frontend with the newly added data.
arcpy.AddMessage("End of the import of the glacier edge.")
# TODO: The open attribute table of the glacier edge will not be updated. So far no solution by ArcPy found.
