import win32api
import win32file
import os
from pathlib import Path


class ArtifactFsPath:

    def __init__(self, input_path):
        self.__path = input_path.__str__()
        self.__environvar, self.__subpath, self.__roots = [None, None, None]

    def resolve(self):
        self.__environvar, self.__subpath = self.__splitenvironvar()
        if self.__environvar:
            self.__roots = self.__resolvenvironvar()
        else:
            self.__roots = self.__drives()
        return self

    def __splitenvironvar(self):
        if self.__path[:1] == '%':
            pos2 = self.__path[1:].find('%' + os.path.sep)
            if pos2 > -1:
                return [self.__path[1:1 + pos2], self.__path[2 * '%'.__len__() + os.path.sep.__len__() + pos2:]]
        return ['', self.__path]

    def __resolvenvironvar(self):
        if self.__environvar == 'ProgramFiles':
            keyset = ['ProgramFiles', 'ProgramFiles(x86)', 'ProgramW6432']
        else:
            keyset = [self.__environvar]
        keyset = [k.upper() for k in keyset]
        ret = list()
        for k in os.environ.keys():
            if k.upper() in keyset:
                if os.environ[k] is not None and os.environ[k] != '' and os.environ[k] not in ret:
                    ret.append(os.environ[k])
        return ret

    @staticmethod
    def __drives():
        ret = list()
        for drive in win32api.GetLogicalDriveStrings().split('\\\000')[:-1]:
            if win32file.GetDriveType(drive) in {win32file.DRIVE_FIXED, win32file.DRIVE_REMOVABLE}:
                ret.append(drive)
        return sorted(ret)

    def findpath(self):
        if self.__roots is None:
            self.resolve()
        ret = list()
        for root in self.__roots:
            try:
                for match in Path(root + os.path.sep).glob(self.__subpath):
                    ret.append(match)
            except NotImplementedError:  # non-relative path as a glob() param are unsupported
                pass
        return ret
