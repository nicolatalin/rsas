from .const import CONST
from src.db.db import DB
from .app import App


class AppsDB:

    def __init__(self):
        self.__dbfilepath = CONST.DB_PATH()
        self.__apps = None
        self.__numapps = None
        self.__numdetectedapps = None

    def dbpath(self):
        return self.__dbfilepath

    def __dbconn(self):
        return DB(self.__dbfilepath)

    def __getapps(self):
        db = self.__dbconn()
        if not db.error:
            apps = list()
            for app in db.getApps():
                apps.append(App(app, db.getArtifacts(app['id'])))
            db.close()
            return apps
        return False

    def apps(self):
        if self.__apps is None:
            self.__apps = self.__getapps()
        return self.__apps

    def error(self):
        return True if self.apps() is False else False

    def __do_count_detected(self):
        count = 0
        for app in self.apps().__iter__():
            if app.detected():
                count += 1
        return count

    def countdetected(self):
        if self.__numdetectedapps is None:
            self.__numdetectedapps = self.__do_count_detected()
        return self.__numdetectedapps

    def __do_count_apps(self):
        count = 0
        for app in self.apps().__iter__():
            if app.artnumtot():
                count += 1
        return count

    def numapps(self):
        if self.__numapps is None:
            self.__numapps = self.__do_count_apps()
        return self.__numapps
