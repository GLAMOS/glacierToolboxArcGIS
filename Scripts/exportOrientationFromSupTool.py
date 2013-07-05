'''
Created on 05.07.2013

@author: yvow
'''

import arcpy, photogrammetry.exportOrientationFromSup

inputDirectory = arcpy.GetParameterAsText(0)
exportFile = arcpy.GetParameterAsText(1)

arcpy.AddMessage("Start to parse the sup files ...")

photogrammetry.exportOrientationFromSup.doExport(inputDirectory, exportFile)

arcpy.AddMessage("End of parsing the sup files.")
