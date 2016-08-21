import winreg
import fnmatch
from .regval import RegVal
import os.path


class RegKey:

    def __init__(self, keypath):
        if keypath.endswith('\\') or keypath.endswith('//'):
            keypath = os.path.dirname(keypath)
        self.__keypath = keypath
        self.__tree = None
        self.__mainkeys = {
            'HKU': winreg.HKEY_USERS,
            'HKCU': winreg.HKEY_CURRENT_USER,
            'HKCR': winreg.HKEY_CLASSES_ROOT,
            'HKLM': winreg.HKEY_LOCAL_MACHINE,
            'HKPD': winreg.HKEY_PERFORMANCE_DATA,
            'HKCC': winreg.HKEY_CURRENT_CONFIG,
            'HKDD': winreg.HKEY_DYN_DATA
        }

    def path(self):
        return self.__keypath

    def basename(self):
        return os.path.basename(self.path())

    def dirname(self):
        return os.path.dirname(self.path())

    def __buildtree(self):
        str = self.path()
        tree = list()
        while str.__len__():
            k = RegKey(str)
            tree.append(k)
            str = k.dirname()
        tree.reverse()
        return tree

    def tree(self):
        if self.__tree is None:
            self.__tree = self.__buildtree()
        return self.__tree

    def find(self):
        if '*' not in self.path():
            return [self]
        else:
            for t in self.tree():
                if '*' in t.basename():
                    ret = list()
                    if t.dirname() == '':
                        for c in [RegKey(k) for k in self.__mainkeys]:
                            ret.extend(c.child(self.path()[t.path().__len__():].strip("\\")).find())
                    else:
                        p = RegKey(t.dirname())
                        if p.open().exists():
                            for c in p.subkeysfilter(t.basename()):
                                ret.extend(c.child(self.path()[t.path().__len__():].strip("\\")).find())
                    return ret
        return list()

    def child(self, subpath):
        return RegKey(os.path.join(self.path(), subpath))

    def __splitmainsub(self):
        keyparts = self.path().split('\\', 1)
        return [self.__mainkeys[keyparts[0].upper()], keyparts[1] if keyparts.__len__() > 1 else '']

    def open(self):
        try:
            [mainkey, subkey] = self.__splitmainsub()
            winreg.ConnectRegistry(None, mainkey)
            self.__hkey = winreg.OpenKey(mainkey, subkey)
            self.__keyexists = True
        except:
            self.__keyexists = False
        return self

    def exists(self):
        return self.__keyexists

    def valuesfilter(self, valuenamepattern):
        ret = list()
        for v in self.values():
            if fnmatch.fnmatch(v.name(), valuenamepattern):
                ret.append(v)
        return ret

    def subkeysfilter(self, pattern):
        ret = list()
        for sk in self.subkeys():
            if fnmatch.fnmatch(sk.basename(), pattern):
                ret.append(sk)
        return ret

    def values(self):
        return [RegVal(v[0], v[2], v[1]) for v in self.__getcontent('v')]

    def subkeys(self):
        return [self.child(sk) for sk in self.__getcontent('k')]

    def __getcontent(self, type):
        ret = list()
        try:
            i = 0
            while True:
                ret.append(winreg.EnumKey(self.__hkey, i) if type == 'k' else winreg.EnumValue(self.__hkey, i))
                i += 1
        except OSError:
            pass
        return ret

