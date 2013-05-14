import arcpy, uuid, ConfigParser, datetime, getpass, os

DATABASE_MAPPING_FILE = "GlacierDatabaseMapping.cfg"

class ImportHelper(object):

    def __init__(self):
        databaseMappingFile = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")), DATABASE_MAPPING_FILE)
        self.__databaseMapping = ConfigParser.RawConfigParser()
        self.__databaseMapping.read(databaseMappingFile)

    def __del__(self):
        pass
    
    def setImportDetails(self, row):

        newPrimaryKey = '{' + str(uuid.uuid1()) + '}'
        
        row.setValue(self.__databaseMapping.get('AllTable', 'PrimaryKey'), newPrimaryKey)
        
        now = datetime.datetime.now()

        row.setValue(self.__databaseMapping.get('AllTable', 'Date_Of_Creation'), now)
        row.setValue(self.__databaseMapping.get('AllTable', 'Created_By'), getpass.getuser())

        return newPrimaryKey

    def getDatabaseMapping(self, group, key):
        return self.__databaseMapping.get(group, key)
