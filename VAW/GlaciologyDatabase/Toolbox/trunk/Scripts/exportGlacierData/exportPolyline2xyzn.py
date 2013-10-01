import arcpy

CODE_LINE_START = 21
CODE_LINE_VERTEX = 22
CODE_LINE_END = 23
CODE_POINT = 11

def doExport(sourceLayer, targetFile):
    arcpy.AddMessage("Start to export a line layer to a xyzn ASCII file ...")
    arcpy.AddMessage("Source layer: " + str(sourceLayer))
    arcpy.AddMessage("Target file: " + targetFile)

    analyzedLines = analyzeLines(sourceLayer)
    exportAnalyzedLines(analyzedLines, targetFile)


def analyzeLines(sourceLayer):
    """
    Analyzes individual polylines and stores the three vertex coordinates in individual arrays.
    """

    fcVertexList = []

    dsc = arcpy.Describe(sourceLayer)
    shapeFieldName = dsc.ShapeFieldName

    arcpy.AddMessage("Shape field name: " + shapeFieldName)

    featureNumber = 0
    searchRows = arcpy.SearchCursor(sourceLayer)

    for searchRow in searchRows:
        shapeObj = searchRow.getValue(shapeFieldName)
        
        arcpy.AddMessage("A new geometry will be analyzed.")
        
        if shapeObj.type == "point":
            arcpy.AddMessage("A new point geometry was found.")
            
            featureNumber = featureNumber + 1
            fcVertexList.append([])
            
            fcVertexList[featureNumber - 1].append([shapeObj.getPart().X, shapeObj.getPart().Y, shapeObj.getPart().Z])
            
            
            
        elif (shapeObj.type == "polygon" or shapeObj.type == "polyline"):
            # Loop for MultiPart
            for partObj in shapeObj:
                
                arcpy.AddMessage("A new part within the current geometry was found.")
                featureNumber = featureNumber + 1
                fcVertexList.append([])
                
                for pointObj in partObj:
                    # Handling only valid geometries.
                    if (pointObj != None):
                        fcVertexList[featureNumber - 1].append([pointObj.X, pointObj.Y, pointObj.Z])
        
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
