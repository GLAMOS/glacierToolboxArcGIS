import arcpy

def doConversion(glacierEdgeLayer, glacierAreaLayer):

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
        array = arcpy.Array()

        for vertex in vertexList:
            point.X = vertex[0]
            point.Y = vertex[1]
            point.Z = vertex[2]
            array.append(point)
        # Add the first point of the array in to close off the polygon
        #array.add(array.getObject(0))

        # Analyse possibly existing islands of the glacier
        islandVertexList = []
        islandVertexList = analyseIsland(dscGlacierEdgeLayer, glacierEdge)

        i = 0
        for islandVertex in islandVertexList:
            i = i + 1
            arcpy.AddMessage("Found island: " + str(i))

            arcpy.AddMessage(islandVertex)

            array.append(arcpy.Point(None, None, None))

            for vertex in islandVertex:
                array.append(arcpy.Point(vertex[0], vertex[1], vertex[2]))

            if i == 1:
                break

            

        # Create a Polygon object based on the array of points
        polygon = arcpy.Polygon(array)

        # Clear the array for future use
        array.removeAll()

        insertArea(glacierAreaLayer, polygon)
        

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

        

def insertArea(glacierAreaLayer, polygon):

    dscGlacierAreaLayer = arcpy.Describe(glacierAreaLayer)
    glacierAreaShapeFieldName = dscGlacierAreaLayer.ShapeFieldName

    try:

        glacierAreas = arcpy.InsertCursor(glacierAreaLayer)
        newGlacierArea = glacierAreas.newRow()
        
        newGlacierArea.setValue(glacierAreaShapeFieldName, polygon)
        
        glacierAreas.insertRow(newGlacierArea)

        del newGlacierArea
        del glacierAreas
        
    except Exception as e:
        arcpy.AddMessage("Error during insert geometries:\n" + e.message)

    finally:
        pass

