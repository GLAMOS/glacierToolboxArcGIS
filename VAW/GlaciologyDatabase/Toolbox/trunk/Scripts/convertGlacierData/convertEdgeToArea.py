import arcpy, os, sys

lib_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")), "helper")
sys.path.append(lib_path)
arcpy.AddMessage(lib_path)
import importHelper

def doConversion(glacierEdgeLayer, glacierAreaLayer):

    objImportHelper = importHelper.ImportHelper()

    # Loop through all the selected, or all, objects of the source layer
    glacierEdges = arcpy.SearchCursor(glacierEdgeLayer)

    dscGlacierEdgeLayer = arcpy.Describe(glacierEdgeLayer)
    glacierEdgeShapeFieldName = dscGlacierEdgeLayer.ShapeFieldName

    for glacierEdge in glacierEdges:

        # Empty vertex array
        vertexList = []

        shapeObj = glacierEdge.getValue(glacierEdgeShapeFieldName)
        # TODO: Handle multi-part feature
        partObj = shapeObj.getPart(0)
        for pointObj in partObj:
            vertexList.append([pointObj.X, pointObj.Y, pointObj.Z])

        arcpy.AddMessage(vertexList)

        point = arcpy.Point()
        mainPart = arcpy.Array()

        allParts = arcpy.Array()

        for vertex in vertexList:
            point.X = vertex[0]
            point.Y = vertex[1]
            point.Z = vertex[2]
            mainPart.append(point)

        allParts.append(mainPart)

        # Analyse possibly existing islands of the glacier
        islandVertexLists = []
        islandVertexLists = analyseIsland(dscGlacierEdgeLayer, glacierEdge)

        i = 0
        for islandVertexList in islandVertexLists:
            i = i + 1
            arcpy.AddMessage("Found island: " + str(i))

            arcpy.AddMessage(islandVertexList)

            islandPart = arcpy.Array()

            for islandVertex in islandVertexList:
                islandPart.append(arcpy.Point(islandVertex[0], islandVertex[1], islandVertex[2]))

            allParts.append(islandPart)
            

        # Create a Polygon object based on the array of points
        polygon = arcpy.Polygon(allParts)

        newGuid = insertArea(objImportHelper, glacierEdge, glacierAreaLayer, polygon)

        setConversionInformation(dscGlacierEdgeLayer, glacierEdge, newGuid)

    del glacierEdge
    del glacierEdges

def analyseIsland(dscGlacierEdgeLayer, glacierEdge):
    arcpy.AddMessage("Datasource: " + dscGlacierEdgeLayer.catalogPath)
    glacierEdgeShapeFieldName = dscGlacierEdgeLayer.ShapeFieldName

    # Reading the key values of the input edge record.
    pk = glacierEdge.getValue("PK")
    fkGlacier = glacierEdge.getValue("FK_Glacier")
    measureDate = glacierEdge.getValue("MeasureDate")

    sqlStatement = "PK <> " + pk + " AND FK_Glacier = " + str(fkGlacier) + " AND MeasureDate = #" + str(measureDate) + "#"

    relatedGlacierEdges = arcpy.SearchCursor(dscGlacierEdgeLayer.catalogPath, sqlStatement)

    # List of all individual island geometries.
    islandVertexList = []

    i = 0
    for relatedGlacierEdge in relatedGlacierEdges:
        i = i + 1
        arcpy.AddMessage("Found related edge geometry: " + str(i) + "\nStart analysing island geometry.")

        vertexList = []

        shapeObj = relatedGlacierEdge.getValue(glacierEdgeShapeFieldName)
        # TODO: Handle multi-part feature
        partObj = shapeObj.getPart(0)
        for pointObj in partObj:
            vertexList.append([pointObj.X, pointObj.Y, pointObj.Z])

        islandVertexList.append(vertexList)

    arcpy.AddMessage("End analysing island geometries")

    return islandVertexList

        

def insertArea(objImportHelper, originalGlacierEdge, glacierAreaLayer, polygon):

    dscGlacierAreaLayer = arcpy.Describe(glacierAreaLayer)
    glacierAreaShapeFieldName = dscGlacierAreaLayer.ShapeFieldName

    try:

        glacierAreas = arcpy.InsertCursor(glacierAreaLayer)
        newGlacierArea = glacierAreas.newRow()

        # Set the geometry
        newGlacierArea.setValue(glacierAreaShapeFieldName, polygon)

        # Copy the original values
        newGlacierArea.setValue("FK_Glacier", originalGlacierEdge.getValue("FK_Glacier"))
        newGlacierArea.setValue("MeasureDate", originalGlacierEdge.getValue("MeasureDate"))
        newGlacierArea.setValue("SubName", originalGlacierEdge.getValue("SubName"))

        # Setting the general attributes.
        newGuid = objImportHelper.setImportDetails(newGlacierArea)
        
        glacierAreas.insertRow(newGlacierArea)

        del newGlacierArea
        del glacierAreas

        arcpy.AddMessage("Newly created glacier area:" + str(newGuid))

        return newGuid
        
    except Exception as e:
        arcpy.AddMessage("Error during insert geometries:\n" + e.message)

    finally:
        pass

def setConversionInformation(dscGlacierEdgeLayer, glacierEdge, newGuid):
    
    fkGlacier = glacierEdge.getValue("FK_Glacier")
    measureDate = glacierEdge.getValue("MeasureDate")

    sqlStatement = "FK_Glacier = " + str(fkGlacier) + " AND MeasureDate = #" + str(measureDate) + "#"

    originalGlacierEdges = arcpy.UpdateCursor(dscGlacierEdgeLayer.catalogPath, sqlStatement)

    for originalGlacierEdge in originalGlacierEdges:
        originalGlacierEdge.setValue("FK_Area", newGuid)

        originalGlacierEdges.updateRow(originalGlacierEdge)
        


    
































    
