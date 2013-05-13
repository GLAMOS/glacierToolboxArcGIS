import arcpy, ConfigParser, os, importHelper

def doImport(targetLayer, sourceLayer, glacierId, measureDate, subName):

    subNameTemp = subName
    if len(subName) == 0:
        subNameTemp = "<NULL>"

    message = "Given import parameter:\nTarget layer: %s\nSource layer: %s\nGlacier ID: %s\nMeasure Date: %s\nSub name: %s" \
    % (targetLayer, sourceLayer, glacierId, measureDate, subNameTemp)
    arcpy.AddMessage(message)

    sourceLayerRows = arcpy.SearchCursor(sourceLayer)
    targetLayerRows = arcpy.InsertCursor(targetLayer)
    
    descSourceLayer = arcpy.Describe(sourceLayer)
    shapeFieldNameSourceLayer = descSourceLayer.ShapeFieldName
    descTargetLayer = arcpy.Describe(targetLayer)
    shapeFieldNameTargetLayer = descTargetLayer.ShapeFieldName

    # Helper for general import management
    objImportHelper = importHelper.ImportHelper()

    for sourceLayerRow in sourceLayerRows: 

        targetLayerRow = targetLayerRows.newRow()

        targetLayerRow.setValue(shapeFieldNameTargetLayer, sourceLayerRow.getValue(shapeFieldNameSourceLayer))
        targetLayerRow.setValue(objImportHelper.getDatabaseMapping('Glacier', 'Edge_ForeignKey_Glacier'), glacierId)
        targetLayerRow.setValue(objImportHelper.getDatabaseMapping('Glacier', 'Edge_MeasureDate'), measureDate)

        if len(subName) > 0:
            targetLayerRow.setValue(objImportHelper.getDatabaseMapping('Glacier', 'Edge_SubName'), subName)

        # Set all the general options of the import.
        objImportHelper.setImportDetails(targetLayerRow)
        
        targetLayerRows.insertRow(targetLayerRow)

    del targetLayerRow
    del targetLayerRows
    del sourceLayerRow
    del sourceLayerRows


