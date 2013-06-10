'''
Created on 10.06.2013

@author: Yvo
'''

import arcpy, os

class TableConversion(object):
    
    def __init__(self, sourceTable, targetTable):
        self._sourceTable = sourceTable
        self._targetTable = targetTable
        
    def SourceTable(self):
        return self._sourceTable
    
    def TargetTable(self):
        return self._targetTable

def doCopy(sourceDatabase, targetDatabase):
    
    tableConversions = []
    
    sourceFeatureDataset = ""
    targetFeatureDataset = ""
    
    tableConversions.append(TableConversion(sourceFeatureDataset + os.sep + "Glacier", targetFeatureDataset + os.sep + "Glacier"))
    tableConversions.append(TableConversion(sourceFeatureDataset + os.sep + "AreaOfInterest", targetFeatureDataset + os.sep + "AreaOfInterest"))
    tableConversions.append(TableConversion(sourceFeatureDataset + os.sep + "Organisation", targetFeatureDataset + os.sep + "Organisation"))
    tableConversions.append(TableConversion(sourceFeatureDataset + os.sep + "ContactPerson", targetFeatureDataset + os.sep + "ContactPerson"))
    tableConversions.append(TableConversion(sourceFeatureDataset + os.sep + "ObjectAuthor", targetFeatureDataset + os.sep + "ObjectAuthor"))
    
    sourceFeatureDataset = "Glacier"
    targetFeatureDataset = "Glacier"
    
    tableConversions.append(TableConversion(sourceFeatureDataset + os.sep + "Area", targetFeatureDataset + os.sep + "Area"))
    tableConversions.append(TableConversion(sourceFeatureDataset + os.sep + "ContureLine", targetFeatureDataset + os.sep + "ContureLine"))
    tableConversions.append(TableConversion(sourceFeatureDataset + os.sep + "Edge", targetFeatureDataset + os.sep + "Edge"))
    tableConversions.append(TableConversion(sourceFeatureDataset + os.sep + "Mouth", targetFeatureDataset + os.sep + "Mouth"))
    tableConversions.append(TableConversion(sourceFeatureDataset + os.sep + "Tongue", targetFeatureDataset + os.sep + "Tongue"))
    
    schemaType = "TEST"
    fieldMappings = ""
    subtype = ""
    
    for tableConversion in tableConversions:
        
        source = sourceDatabase + os.sep + tableConversion.SourceTable()
        target = targetDatabase + os.sep + tableConversion.TargetTable()
                
        arcpy.AddMessage("Start to copy from '{0}' to '{1}'.".format(source, target))
        
        arcpy.Append_management(source, target, schemaType, fieldMappings, subtype)
        
        arcpy.AddMessage("End of copy from '{0}' to '{1}'.".format(source, target))