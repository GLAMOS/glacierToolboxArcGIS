'''
Created on 05.07.2013

@author: yvow
'''

import arcpy

__DELIMITER = "\t"

def doExport(inputGcpLayer, idField, exportFile):
    
    analyzedGcpList = analyzeGcp(inputGcpLayer, idField)
    
    writeGcpFile(analyzedGcpList, exportFile)

def analyzeGcp(inputGcpLayer, idField):
    
    gcpList = []
    
    dsc = arcpy.Describe(inputGcpLayer)
    shapeFieldName = dsc.ShapeFieldName

    arcpy.AddMessage("Shape field name: " + shapeFieldName)

    searchRows = arcpy.SearchCursor(inputGcpLayer)
    for searchRow in searchRows:
        
        gcpId = searchRow.getValue(str(idField))
       
        gcp = searchRow.getValue(shapeFieldName)
        pnt = gcp.getPart()

        arcpy.AddMessage("GCP found: " + str(gcpId) + " -> " + str(pnt.X) + " / " + str(pnt.Y) + " (" + str(pnt.Z) + ")")
        
        gcpList.append([gcpId, pnt.X, pnt.Y, pnt.Z])
        
    return gcpList

def writeGcpFile(gcpList, exportFile):
    
    f = open(exportFile, 'a')
    
    for gcp in gcpList:
        
        lineToWrite = str(gcp[0]) + __DELIMITER + str(gcp[1]) + __DELIMITER + str(gcp[2]) + __DELIMITER + str(gcp[3]) + "\n"
        
        f.write(lineToWrite)

    f.close()