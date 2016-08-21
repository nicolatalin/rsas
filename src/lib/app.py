from .artifactrule import ArtifactRule


class App:

    def __init__(self, apprecord, rawartifacts):
        self._nfound = None
        self._record = apprecord
        self._artifacts = list()
        try:
            for art in rawartifacts:
                self._artifacts.append(ArtifactRule(art))
        except:
            pass

    def name(self):
        return self._record['name']

    def artnumtot(self):
        return self._artifacts.__len__()

    def detected(self):
        return self.artnumtot() and self.artnumfound() > 0

    def artnumfound(self):
        if self._nfound is None:
            self.findartifacts()
        return self._nfound

    def findartifacts(self):
        if self.artnumtot():
            self._nfound = 0
            for art in self._artifacts:
                if art.exists():
                    self._nfound += 1
        return self

    def getartifacts(self):
        return self._artifacts