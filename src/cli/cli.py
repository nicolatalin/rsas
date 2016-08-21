from src.lib.scanner import Scanner
from src.lib.const import CONST


class CLI:

    @classmethod
    def CMDs(cls):
        return {
            'quit': {
                'desc': 'quit this software'
            },
            'help': {
                'desc': 'print help on this software',
                'op': lambda: cls.__help()
            },
            'about': {
                'desc': 'print information about this software and its authors',
                'op': lambda: print(CONST.PROG_ABOUT)
            },
            'dbprintapps': {
                'desc': 'print list of apps in DB',
                'op': lambda: print(Scanner().printapps().str())
            },
            'dbprintarts': {
                'desc': 'print list of artifacts in DB',
                'op': lambda: print(Scanner().printartifacts().str())
            },
            'scan': {
                'desc': 'scan system for artifacts',
                'op': lambda: print(Scanner().scan(1).str())
            },
            'scanv': {
                'desc': 'scan system for artifacts (verbose)',
                'op': lambda: print(Scanner().scan(3).str())
            },
            'scanvv': {
                'desc': 'scan system for artifacts (very verbose)',
                'op': lambda: print(Scanner().scan(4).str())
            }
        }

    @classmethod
    def __help(cls):
        for k, v in sorted(cls.CMDs().items()):
            print(k + ' - ' + v['desc'])

    @staticmethod
    def __cmdprompt():
        return input('> ')

    @classmethod
    def console(cls):
        print(CONST.PROG_LONGNAME)
        cmd = None
        while cmd != 'quit':
            cls.do(cmd)
            cmd = cls.__cmdprompt()
        print('Goodbye!')

    @classmethod
    def do(cls, cmd):
        if cmd in cls.CMDs():
            if 'op' in cls.CMDs()[cmd]:
                # try:
                    cls.CMDs()[cmd]['op']()
                # except:
                #    print('Command execution failed.')
        elif cmd is not None and cmd != "":
            print("Unknown command. Use command 'help' to know more.")
