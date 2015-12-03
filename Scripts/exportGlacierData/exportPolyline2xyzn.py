import arcpy

CODE_LINE_START = 21
CODE_LINE_VERTEX = 22
CODE_LINE_END = 23
CODE_POINT = 11

CODE_NaN = "NaN"

def doExport(sourceLayer, targetFile, altitudeField, pointIdField):
    arcpy.AddMessage("Start to export a line layer to a xyzn ASCII file ...")
    arcpy.AddMessage("Source layer: " + str(sourceLayer))
    arcpy.AddMessage("Target file: " + targetFile)

    analyzedLines = analyzeLines(sourceLayer, altitudeField, pointIdField)
    exportAnalyzedLines(analyzedLines, targetFile)


def analyzeLines(sourceLayer, altitudeField, pointIdField):
    """
    Analyzes individual polylines and stores the three vertex coordinates in individual arrays.
    """
    
    try:

        fcVertexList = []

        dsc = arcpy.Describe(sourceLayer)
        shapeFieldName = dsc.ShapeFieldName

        arcpy.AddMessage("Shape field name: " + shapeFieldName)
        arcpy.AddMessage("Altitude field name: ->" + altitudeField + "<-")

        featureNumber = 0
        searchRows = arcpy.SearchCursor(sourceLayer)

        for searchRow in searchRows:
            shapeObj = searchRow.getValue(shapeFieldName)
            
            if altitudeField == "":
                pass
            else:
                altitude = searchRow.getValue(altitudeField)
            
            arcpy.AddMessage("A new geometry will be analyzed.")
            
            if shapeObj.type == "point":
                arcpy.AddMessage("A new point geometry was found.")
                
                if pointIdField == "":
                    pass
                else:
                    pointId = searchRow.getValue(pointIdField)
                
                featureNumber = featureNumber + 1
                fcVertexList.append([])
                           
                if altitudeField != "":
                    if pointIdField != "":
                        fcVertexList[featureNumber - 1].append([pointId, shapeObj.getPart().X, shapeObj.getPart().Y, altitude])
                    else:
                        fcVertexList[featureNumber - 1].append([shapeObj.getPart().X, shapeObj.getPart().Y, altitude])
                else:
                
                    # Replacing the Python None with the Wave NaN for better processing internaly at VAW.
                    zValue = CODE_NaN
                    if shapeObj.getPart().Z != None:
                        zValue = shapeObj.getPart().Z
                    
                    if pointIdField != "":
                        fcVertexList[featureNumber - 1].append([pointId, shapeObj.getPart().X, shapeObj.getPart().Y, zValue])
                    else:
                        fcVertexList[featureNumber - 1].append([shapeObj.getPart().X, shapeObj.getPart().Y, zValue])
                    
                
            elif (shapeObj.type == "polygon" or shapeObj.type == "polyline"):
                # Loop for MultiPart
                
                arcpy.AddMessage("A new geometry was found.")
                featureNumber = featureNumber + 1
                fcVertexList.append([])
      
                for partObj in shapeObj:
                    
                    arcpy.AddMessage("A new part within the current geometry was found.")
                    
                    for pointObj in partObj:
                        # Handling only valid geometries.
                        if (pointObj != None):
                        
                            # Replacing the Python None with the Wave NaN for better processing internaly at VAW.
                            zValue = CODE_NaN
                            if pointObj.Z != None:
                                zValue = pointObj.Z
                            
                            if  altitudeField == "":
                                fcVertexList[featureNumber - 1].append([pointObj.X, pointObj.Y, zValue])
                            else:
                                fcVertexList[featureNumber - 1].append([pointObj.X, pointObj.Y, altitude])
            
            else:
                arcpy.AddMessage("The current type of geometry is not handled.")


        return fcVertexList
        
    except:
        arcpy.AddMessage("ERROR")

def exportAnalyzedLines(analyzedLines, targetFile):

    exportFile = open(targetFile, 'w')

    try:

        for analyzedLine in analyzedLines:

            numberVertex = len(analyzedLine)

            arcpy.AddMessage("Geometry with " + str(numberVertex) + " vertex found.")

            for i in range(0, numberVertex):

                if numberVertex == 1:
                    
                    codeVertex = CODE_POINT
                
                else:
                    
                    codeVertex = CODE_LINE_VERTEX
    
                    if i == 0:
                        codeVertex = CODE_LINE_START
                    elif i == numberVertex - 1:
                        codeVertex = CODE_LINE_END

                lineToWrite = ""
                j = 0
                while j < len(analyzedLine[i]):
                    lineToWrite = lineToWrite + str(analyzedLine[i][j]) + " "
                    j = j + 1
                
                lineToWrite = lineToWrite + str(codeVertex)
                    
                arcpy.AddMessage("Vertex found: " + lineToWrite)
                exportFile.write(lineToWrite + "\n")

    except:
        arcpy.AddMessage("Export failed!")

    finally:
        exportFile.close()
