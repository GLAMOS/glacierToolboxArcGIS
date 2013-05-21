import arcpy, os, sys

lib_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")), "helper")
sys.path.append(lib_path)
arcpy.AddMessage(lib_path)
import databaseHelper

def doConversion(glacierEdgeLayer, glacierAreaLayer):

    objDatabaseHelper = databaseHelper.DatabaseHelper()

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
        islandVertexLists = analyseIsland(objDatabaseHelper, dscGlacierEdgeLayer, glacierEdge)

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

        newGuid = insertArea(objDatabaseHelper, glacierEdge, glacierAreaLayer, polygon)

        setConversionInformation(objDatabaseHelper, dscGlacierEdgeLayer, glacierEdge, newGuid)

    del glacierEdge
    del glacierEdges

def analyseIsland(objDatabaseHelper, dscGlacierEdgeLayer, glacierEdge):
    arcpy.AddMessage("Datasource: " + dscGlacierEdgeLayer.catalogPath)
    glacierEdgeShapeFieldName = dscGlacierEdgeLayer.ShapeFieldName

    # Reading the key values of the input edge record.
    pkFieldName = objDatabaseHelper.getDatabaseMapping("AllTable", "PrimaryKey")
    pk = glacierEdge.getValue(pkFieldName)
    fkGlacierFieldName = objDatabaseHelper.getDatabaseMapping("Glacier", "Edge_ForeignKey_Glacier")
    fkGlacier = glacierEdge.getValue(fkGlacierFieldName)
    measureDateFieldName = objDatabaseHelper.getDatabaseMapping("Glacier", "Edge_MeasureDate")
    measureDate = glacierEdge.getValue(measureDateFieldName)

    # Construction of the SQL statement and setup of the search cursor to retrieve all the island edges.
    sqlStatement = "{0} <> {1} AND {2} = {3} AND {4} = #{5}#".format(pkFieldName, pk, fkGlacierFieldName, str(fkGlacier), measureDateFieldName, str(measureDate))
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

        

def insertArea(objDatabaseHelper, originalGlacierEdge, glacierAreaLayer, polygon):

    dscGlacierAreaLayer = arcpy.Describe(glacierAreaLayer)
    glacierAreaShapeFieldName = dscGlacierAreaLayer.ShapeFieldName

    try:

        glacierAreas = arcpy.InsertCursor(glacierAreaLayer)
        newGlacierArea = glacierAreas.newRow()

        # Set the geometry
        newGlacierArea.setValue(glacierAreaShapeFieldName, polygon)

        # Copy the original values
        fkGlacierFieldNameArea = objDatabaseHelper.getDatabaseMapping("Glacier", "Area_ForeignKey_Glacier")
        fkGlacierFieldNameEdge = objDatabaseHelper.getDatabaseMapping("Glacier", "Edge_ForeignKey_Glacier")
        newGlacierArea.setValue(fkGlacierFieldNameArea, originalGlacierEdge.getValue(fkGlacierFieldNameEdge))
        measureDateFieldNameArea = objDatabaseHelper.getDatabaseMapping("Glacier", "Area_MeasureDate")
        measureDateFieldNameEdge = objDatabaseHelper.getDatabaseMapping("Glacier", "Edge_MeasureDate")
        newGlacierArea.setValue(measureDateFieldNameArea, originalGlacierEdge.getValue(measureDateFieldNameEdge))
        subNameFieldNameArea = objDatabaseHelper.getDatabaseMapping("Glacier", "Area_SubName")
        subNameFieldNameEdge = objDatabaseHelper.getDatabaseMapping("Glacier", "Edge_SubName")
        newGlacierArea.setValue(subNameFieldNameArea, originalGlacierEdge.getValue(subNameFieldNameEdge))

        # Setting the general attributes.
        newGuid = objDatabaseHelper.setImportDetails(newGlacierArea)
        
        glacierAreas.insertRow(newGlacierArea)

        del newGlacierArea
        del glacierAreas

        arcpy.AddMessage("Newly created glacier area:" + str(newGuid))

        return newGuid
        
    except Exception as e:
        arcpy.AddMessage("Error during insert geometries:\n" + e.message)

    finally:
        pass

def setConversionInformation(objDatabaseHelper, dscGlacierEdgeLayer, glacierEdge, newGuid):

    fkGlacierFieldName = objDatabaseHelper.getDatabaseMapping("Glacier", "Edge_ForeignKey_Glacier")
    fkGlacier = glacierEdge.getValue(fkGlacierFieldName)
    measureDateFieldName = objDatabaseHelper.getDatabaseMapping("Glacier", "Edge_MeasureDate")
    measureDate = glacierEdge.getValue(measureDateFieldName)

    sqlStatement = "FK_Glacier = " + str(fkGlacier) + " AND MeasureDate = #" + str(measureDate) + "#"
    sqlStatement2 = "{0} = {1} AND {2} = #{3}#".format(fkGlacierFieldName, str(fkGlacier), measureDateFieldName, str(measureDate))

    originalGlacierEdges = arcpy.UpdateCursor(dscGlacierEdgeLayer.catalogPath, sqlStatement2)

    fkAreaFieldName = objDatabaseHelper.getDatabaseMapping("Glacier", "Edge_ForeignKey_Area")

    for originalGlacierEdge in originalGlacierEdges:
        originalGlacierEdge.setValue(fkAreaFieldName, newGuid)

        originalGlacierEdges.updateRow(originalGlacierEdge)
        


    
































    
