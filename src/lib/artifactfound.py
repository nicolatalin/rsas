from .regval import RegVal


class ArtifactFound:

    def __init__(self, path, values=list()):
        self.__path = path
        self.__values = values # expected type: list of RegVal

    def path(self):
        return self.__path

    def values(self):
        return self.__values
