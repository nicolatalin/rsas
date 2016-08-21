from .artifactfspath import ArtifactFsPath
from .regkey import RegKey
from .artifactfound import ArtifactFound


class ArtifactRule:

    def __init__(self, record):
        self.__path = record['path']
        self.__type = record['type']
        self.__val = record['val']
        self.__searchresults = None

    def path(self):
        return self.__path

    def type(self):
        return self.__type

    def val(self):
        return self.__val

    def __search(self):
        ret = list()
        if 1000 < self.type() < 2000:
            for ar in ArtifactFsPath(self.path()).findpath():
                ret.append(ArtifactFound(ar))
        elif self.type() == 2001:
            for ar in RegKey(self.path()).find():
                if ar.open().exists():
                    ret.append(ArtifactFound(ar.path()))
        elif self.type() == 2002:
            for ar in RegKey(self.path()).find():
                if ar.open().exists():
                    valmatches = ar.valuesfilter(self.val())
                    if valmatches.__len__():
                        ret.append(ArtifactFound(ar.path(), valmatches))
        return ret

    def exists(self):
        if self.__searchresults is None:
            self.__searchresults = self.__search()
        return True if self.__searchresults.__len__() else False

    def res(self):
        if self.__searchresults is None:
            self.__searchresults = self.__search()
        return self.__searchresults
