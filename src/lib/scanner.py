from src.lib.appsdb import AppsDB


class Scanner:

    def __init__(self):
        self.__db = AppsDB()
        out = ''
        if self.__db.error():
            out += 'Connection ' + ('established' if not self.__db.error() else 'failed') + ' with DB: ' + self.__db.dbpath()
        else:
            out += 'DB contains ' + self.__db.numapps().__str__() + ' apps.'
        self.__out = out

    def str(self):
        return self.__out

    def printapps(self):
        out = ''
        if not self.__db.error():
            for app in self.__db.apps():
                if app.artnumtot():
                    out += '\n' + app.name() + ' (' + app.artnumtot().__str__() + ')'
            out += '\n'
        self.__out += out
        return self

    def printartifacts(self):
        out = ''
        if not self.__db.error():
            for app in self.__db.apps():
                if app.artnumtot():
                    out += '\n\n=========================='
                    out += '\nApplication: ' + app.name()
                    for art in app.getartifacts():
                        out += '\n > ' + art.path()
                        if art.type() == 2002:
                            out += '\n    WITH VAL: ' + art.val()
                out += '\n\n'
        self.__out += out
        return self

    def scan(self, verb=3):
        out = ''
        try:
            if not self.__db.error():
                summary = '\nDetected apps: ' + self.__db.countdetected().__str__()
                if self.__db.countdetected():
                    for app in self.__db.apps().__iter__():
                        if app.detected():
                            summary += '\n' + app.name() + ' (' + app.artnumfound().__str__() + '/' + app.artnumtot().__str__() + ')'
                out += summary
                if verb > 1:
                    for app in self.__db.apps().__iter__():
                        if (verb > 3 and app.artnumtot()) or app.detected():
                            out += '\n\n=========================='
                            out += '\nApplication: ' + app.name()
                            if app.detected():
                                out += '\n[ ** DETECTED ** Artifact descriptions matched: ' + app.artnumfound().__str__() + '/' + app.artnumtot().__str__() + ' ]'
                            else:
                                out += '\n[ Not detected ]'
                            for artrule in app.getartifacts():
                                if verb > 2 or artrule.exists():
                                    out += '\n   [' + (
                                    '+' if artrule.exists() else '-') + '] ' + artrule.path().__str__()
                                    if artrule.type() == 2002:
                                        out += '\n       WITH VAL: ' + artrule.val().__str__()
                                    for artfound in artrule.res():
                                        out += '\n          > ' + artfound.path().__str__()
                                        for v in artfound.values():
                                            out += '\n          >> ' + v.name().__str__()
        except PermissionError:
            out += '\n\nThe system is not granting you the permission to read the necessary files. Please run this software as administrator.'
        self.__out += out
        return self
