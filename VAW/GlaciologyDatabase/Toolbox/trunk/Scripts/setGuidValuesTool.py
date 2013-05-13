import arcpy, maintenanceGlacierData.setGuidValues

targetLayer = arcpy.GetParameter(0)
targetField = arcpy.GetParameter(1)

maintenanceGlacierData.setGuidValues.doGuidUpdate(targetLayer, targetField)
