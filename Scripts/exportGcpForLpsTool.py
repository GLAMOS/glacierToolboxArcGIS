'''
Created on 05.07.2013

@author: yvow
'''

import arcpy, photogrammetry.exportGcpForLps

inputGcpLayer = arcpy.GetParameter(0)
idField = arcpy.GetParameter(1)
exportFile = arcpy.GetParameterAsText(2)

arcpy.AddMessage("Start to export GCP's to file ...")

photogrammetry.exportGcpForLps.doExport(inputGcpLayer, idField, exportFile)

arcpy.AddMessage("End of exporting GCP's to file.")
