import os.path as p
import os
import sys


class CONST:

    PROG_SHORTNAME = 'rsas'
    PROG_LONGNAME = 'Removed Steganography Application Scanner'
    PROG_SHORTDESC = 'Finds removed Steganography applications.'

    PROG_ABOUT  =   '---------------------------------------------'
    PROG_ABOUT += '\n| Removed Steganography Application Scanner |'
    PROG_ABOUT += '\n| University of Kent, UK  (2016)            |'
    PROG_ABOUT += '\n| School of Computing  (cs.kent.ac.uk)      |'
    PROG_ABOUT += '\n| Author:     Mr Nicola Talin               |'
    PROG_ABOUT += '\n|             nt271@kent.ac.uk              |'
    PROG_ABOUT += '\n| Supervisor: Dr Julio C. Hernandez-Castro  |'
    PROG_ABOUT += '\n|             jch27@kent.ac.uk              |'
    PROG_ABOUT += '\n---------------------------------------------'

    @staticmethod
    def DB_PATH():
        dbpath = "rsas.sqlite3"
        if getattr(sys, 'frozen', False):
            respath = p.dirname(sys.executable) + "\\" + dbpath
            if not p.exists(respath):
                respath = sys._MEIPASS + "\\" + dbpath
            return respath
        else:
            return p.dirname(p.abspath(__file__)) + "\\..\\..\\data\\" + dbpath
