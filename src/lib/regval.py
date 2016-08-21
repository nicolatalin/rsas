class RegVal:

    def __init__(self, name, type=None, data=None):
        self.__name = name
        self.__type = type
        self.__data = data

    def name(self):
        return self.__name

    def type(self):
        return self.__type

    def data(self):
        return self.__data
