'''
Created on 10.06.2013

@author: Yvo
'''
import arcpy, maintenanceGlacierData.copyDatabase

sourceDatabase = arcpy.GetParameterAsText(0)
targetDatabase = arcpy.GetParameterAsText(1)

maintenanceGlacierData.copyDatabase.doCopy(sourceDatabase, targetDatabase)