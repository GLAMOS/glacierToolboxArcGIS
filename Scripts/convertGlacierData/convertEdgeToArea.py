import arcpy

def doConversion(glacierEdgeLayer, glacierAreaLayer):

    # Loop through all the selected, or all, objects of the source layer
    glacierEdges = arcpy.SearchCursor(glacierEdgeLayer)

    dscGlacierEdgeLayer = arcpy.Describe(glacierEdgeLayer)
    glacierEdgeShapeFieldName = dscGlacierEdgeLayer.ShapeFieldName
    dscGlacierAreaLayer = arcpy.Describe(glacierAreaLayer)
    glacierAreaShapeFieldName = dscGlacierAreaLayer.ShapeFieldName

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
            array.add(point)
        # Add the first point of the array in to close off the polygon
        array.add(array.getObject(0))

        # Create a Polygon object based on the array of points
        polygon = arcpy.Polygon(array)

        # Clear the array for future use
        array.removeAll()

        glacierAreas = arcpy.InsertCursor(glacierAreaLayer)
        glacierArea = glacierAreas.newRow()
        #glacierArea.setValue(glacierAreaShapeFieldName, polygon)
        glacierAreas.insertRow(glacierArea)

        arcpy.AddMessage("Test")

        del glacierArea
        del glacierAreas
        

    del glacierEdge
    del glacierEdges

