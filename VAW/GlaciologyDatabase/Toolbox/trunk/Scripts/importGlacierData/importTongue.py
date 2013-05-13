import arcpy, uuid, ConfigParser, os

DATABASE_MAPPING_FILE = "GlacierDatabaseMapping.cfg"

def doImport(targetLayer, sourceLayer, glacierId, measureDate):
    message = "Given import parameter:\nTarget layer: %s\nSource layer: %s\nGlacier ID: %s\nMeasure Date: %s" \
    % (targetLayer, sourceLayer, glacierId, measureDate)
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
        targetLayerRow.setValue(config.get('Glacier', 'Tongue_PrimaryKey'), '{' + str(uuid.uuid1()) + '}')
        targetLayerRow.setValue(config.get('Glacier', 'Tongue_ForeignKey_Glacier'), glacierId)
        targetLayerRow.setValue(config.get('Glacier', 'Tongue_MeasureDate'), measureDate)
        
        targetLayerRows.insertRow(targetLayerRow)

    del targetLayerRow
    del targetLayerRows
    del sourceLayerRow
    del sourceLayerRows


