import arcpy, uuid

def doGuidUpdate(targetLayer, targetField):

    cur = arcpy.UpdateCursor(targetLayer, str(targetField) + " IS NULL")

    for row in cur:

        arcpy.AddMessage("Old Guid: " + str(row.getValue(str(targetField))))
                         
        row.setValue(str(targetField), '{' + str(uuid.uuid1()) + '}')
        cur.updateRow(row)

        arcpy.AddMessage("New Guid: " + str(row.getValue(str(targetField))))

    del cur, row

