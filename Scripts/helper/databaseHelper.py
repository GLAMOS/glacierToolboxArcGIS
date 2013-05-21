import arcpy, uuid, ConfigParser, datetime, getpass, os

DATABASE_MAPPING_FILE = "GlacierDatabaseMapping.cfg"

DATABASE_TYPE_PERSONALGEODATABASE = "mdb"
DATABASE_TYPE_FILEGEODATABASE = "gdb"
DATABASE_TYPE_SPATIALDATABASEENGINE = "sde"
DATABASE_TYPE_FILEBASED = "shp"

class DatabaseHelper(object):

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

    def getWorkspaceType(self, featureLayer):
        
        workspacePath = featureLayer.workspacePath
        desWorkspacePath = arcpy.Describe(workspacePath)
        workspaceType = desWorkspacePath.workspaceFactoryProgID

        #Identifies File Geodatabase
        if workspaceType == "esriDataSourcesGDB.FileGDBWorkspaceFactory.1":
            return DATABASE_TYPE_FILEGEODATABASE

        #Identifies Personal Geodatabase
        elif workspaceType == "esriDataSourcesGDB.AccessWorkspaceFactory.1":
            return DATABASE_TYPE_PERSONALGEODATABASE

        #Identifies SDE database
        elif workspaceType == "esriDataSourcesGDB.SdeWorkspaceFactory.1":
            return DATABASE_TYPE_SPATIALDATABASEENGINE

        #Other (Shapefile, coverage, CAD, VPF, and so on)
        else:
            return DATABASE_TYPE_FILEBASED
