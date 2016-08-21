from .sqlitedb import SQLiteDB


class DB:

    def __init__(self, path):
        self.filepath = path
        self.sql = SQLiteDB(self.filepath)
        self.error = self.sql.error

    def close(self):
        try:
            self.sql.close()
        except:
            pass

    def getApps(self):
        if self.error:
            return False
        return self.sql.query("SELECT id, name FROM apps ORDER BY name ASC;").rows()

    def getArtifacts(self,appid):
        if self.error:
            return False
        return self.sql.query("SELECT id, path, type, val FROM artifacts WHERE app='"+appid.__str__()+"' ORDER BY type ASC, path ASC, val ASC;").rows()
