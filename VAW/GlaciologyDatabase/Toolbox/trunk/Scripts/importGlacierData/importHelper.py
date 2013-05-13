import arcpy, uuid, ConfigParser, datetime, getpass

# TODO: Import-Helper should be implemented as a class regarding the class-wide
# members such as config or date.

def setImportDetails(row, config):
    
    row.setValue(config.get('AllTable', 'PrimaryKey'), '{' + str(uuid.uuid1()) + '}')
    
    now = datetime.datetime.now()

    row.setValue(config.get('AllTable', 'Date_Of_Creation'), now)
    row.setValue(config.get('AllTable', 'Created_By'), getpass.getuser())
