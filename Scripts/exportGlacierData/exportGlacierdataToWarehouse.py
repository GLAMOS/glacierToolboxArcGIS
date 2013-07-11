# Copyright 2013 GeoIdee, Sandstrasse 2, CH-8003 Zurich
#
# Module     : Scripts.exportGlacierData.exportGlacierdataToWarehouse
# 
# Created by: Yvo
# Created on: 11.07.2013

'''
moduledocs
'''
#TODO: Include module description.

# Imports
import arcpy
from arcpy import env

env.workspace = r"D:\Temp\Glaciology.gdb"

#inFeatures = "AreaOfInterest"
inFeatures = "Glacier/Edge"
joinFieldTarget = "FK_Glacier"
joinTable = "Glacier"
joinFieldSource = "PK"
fieldList = ["ShortName", "RealName", "InventoryNumber"]

arcpy.JoinField_management (inFeatures, joinFieldTarget, joinTable, joinFieldSource, fieldList)

outLocation = "D:/temp"

env.transferDomains = True

arcpy.FeatureClassToShapefile_conversion(inFeatures, outLocation)
