import arcpy

CODE_LINE_START = 21
CODE_LINE_VERTEX = 22
CODE_LINE_END = 23

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
        featureNumber = featureNumber + 1
        fcVertexList.append([])
        shapeObj = searchRow.getValue(shapeFieldName)
       
        # Loop for SinglePart
        #partObj = shapeObj.getPart(0)
        #for pointObj in partObj:
        #    fcVertexList[featureNumber - 1].append([pointObj.X, pointObj.Y, pointObj.Z])
       
        # Loop for MultiPart
        for partObj in shapeObj:
            for pointObj in partObj:
                # Handling only valid geometries.
                if (pointObj != None):
                    fcVertexList[featureNumber - 1].append([pointObj.X, pointObj.Y, pointObj.Z])


    return fcVertexList

def exportAnalyzedLines(analyzedLines, targetFile):

    exportFile = open(targetFile, 'w')

    try:

        for analyzedLine in analyzedLines:

            numberVertex = len(analyzedLine)

            arcpy.AddMessage("Line found with " + str(numberVertex) + " vertex found.")

            for i in range(0, numberVertex):

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
