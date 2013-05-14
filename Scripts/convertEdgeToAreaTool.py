import arcpy, convertGlacierData.convertEdgeToArea

sourceLayer = arcpy.GetParameter(0)
targetLayer = arcpy.GetParameter(0)

convertGlacierData.convertEdgeToArea.doConversion(sourceLayer, targetLayer)

arcpy.RefreshActiveView()

# Refresh the ArcMap frontend with the newly added data.
arcpy.AddMessage("End of the conversion of glacier edge to glacier area.")
# TODO: The open attribute table of the glacier edge will not be updated. So far no solution by ArcPy found.
