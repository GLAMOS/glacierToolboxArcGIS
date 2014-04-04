import arcpy

CODE_LINE_START = 21
CODE_LINE_VERTEX = 22
CODE_LINE_END = 23
CODE_POINT = 11

def doExport(sourceLayer, targetFile, altitudeField):
    arcpy.AddMessage("Start to export a line layer to a xyzn ASCII file ...")
    arcpy.AddMessage("Source layer: " + str(sourceLayer))
    arcpy.AddMessage("Target file: " + targetFile)

    analyzedLines = analyzeLines(sourceLayer, altitudeField)
    exportAnalyzedLines(analyzedLines, targetFile)


def analyzeLines(sourceLayer, altitudeField):
    """
    Analyzes individual polylines and stores the three vertex coordinates in individual arrays.
    """

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
            
            featureNumber = featureNumber + 1
            fcVertexList.append([])
                       
            if altitudeField != "":
                fcVertexList[featureNumber - 1].append([shapeObj.getPart().X, shapeObj.getPart().Y, altitude])
            else:
                fcVertexList[featureNumber - 1].append([shapeObj.getPart().X, shapeObj.getPart().Y, shapeObj.getPart().Z])
            
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
                        
                        if  altitudeField == "":
                            fcVertexList[featureNumber - 1].append([pointObj.X, pointObj.Y, pointObj.Z])
                        else:
                            fcVertexList[featureNumber - 1].append([pointObj.X, pointObj.Y, altitude])
        
        else:
            arcpy.AddMessage("The current type of geometry is not handled.")


    return fcVertexList

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

                lineToWrite = str(analyzedLine[i][0]) + " " + str(analyzedLine[i][1]) + " " + str(analyzedLine[i][2]) + " " + str(codeVertex)
                
                arcpy.AddMessage("Vertex found: " + lineToWrite)
                exportFile.write(lineToWrite + "\n")

    except:
        arcpy.AddMessage("Export failed!")

    finally:
        exportFile.close()
