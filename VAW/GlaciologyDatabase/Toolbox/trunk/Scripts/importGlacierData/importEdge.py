import arcpy, uuid, ConfigParser, os

DATABASE_MAPPING_FILE = "GlacierDatabaseMapping.cfg"

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

    # Open the database mapping file. Regarding the fact that the directory of the file has not to be the current working
    # directory a workaround with the script location had to be implemented.
    databaseMappingFile = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")), DATABASE_MAPPING_FILE)
    config = ConfigParser.RawConfigParser()
    config.read(databaseMappingFile)

    for sourceLayerRow in sourceLayerRows: 

        targetLayerRow = targetLayerRows.newRow()

        targetLayerRow.setValue(shapeFieldNameTargetLayer, sourceLayerRow.getValue(shapeFieldNameSourceLayer))
        targetLayerRow.setValue(config.get('Glacier', 'Edge_PrimaryKey'), '{' + str(uuid.uuid1()) + '}')
        targetLayerRow.setValue(config.get('Glacier', 'Edge_ForeignKey_Glacier'), glacierId)
        targetLayerRow.setValue(config.get('Glacier', 'Edge_MeasureDate'), measureDate)

        if len(subName) > 0:
            targetLayerRow.setValue(config.get('Glacier', 'Edge_SubName'), subName)
        
        targetLayerRows.insertRow(targetLayerRow)

    del targetLayerRow
    del targetLayerRows
    del sourceLayerRow
    del sourceLayerRows


