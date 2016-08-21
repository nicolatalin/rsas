import sqlite3
import os.path


class SQLiteDB:

    def __init__(self, path):
        self.__dbfilepath = path.__str__()
        if os.path.isfile(self.__dbfilepath):
            try:
                self.conn = sqlite3.connect(self.__dbfilepath)
                self.error = False
            except:
                self.error = True
        else:
            self.error = True

    def close(self):
        self.conn.close()

    def query(self, strQuery):
        cur = self.conn.cursor()
        cur.execute(strQuery.__str__())
        return Result(cur)

#    def tbls(self):
#        print self.query("SELECT name FROM sqlite_master WHERE type='table';").fetchall()


class Result:

    def __init__(self, cur):
        self.cursor = cur

    # return list of rows,
    # each row as associative list
    # with column names as keys
    # and corresponding record values as values
    def rows(self):
        rows = list()
        for row in self.cursor.fetchall():
            row2 = dict()
            for i, val in enumerate(row):
                row2[self.cursor.description[i][0]] = val
            rows.append(row2)
        return rows

