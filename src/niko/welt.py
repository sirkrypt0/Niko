from os.path import isfile

class Welt:

    def __init__(self, datei=None, dimension=14):

        self.dimension = dimension
        self.feld = []
        
        if datei:
            self.feld = self.dateiLesen(datei)
        else:
            self.feld = [[0 for i in range(dimension)] for j in range(dimension)]
    
    def dateiLesen(self, datei):
        welt = []
        if isfile(datei):
            datei = open(datei, "r")
            inhalt = datei.readlines()
            for zeile in inhalt:
                zeile = zeile.strip()
                zeile = zeile.split(" ")
                for i in range(len(zeile)):
                    zeile[i] = int(zeile[i])
                welt.append(zeile)
        else:
            welt = [[0 for i in range(dimension)] for j in range(dimension)]
            
        return welt

    def feld_leer(self, x, y):
        if self.feld[y][x] == 0:
            return True
        return False

    def mauerVorhanden(self, x, y):
        if self.feld[y][x] == -1:
            return True
        return False

    def zaehle_Werkzeug(self, x, y):
        if self.feld[y][x] != -1:
            return self.feld[y][x]

    def setze_Mauer(self, x, y):
        if self.feld[y][x] == 0:
            self.feld[y][x] = -1

    def entferne_Mauer(self, x, y):
        if self.feld[y][x] == -1:
            self.feld[y][x] = 0

    def setze_Werkzeug(self, x, y):
        if self.feld[y][x] != -1:
            self.feld[y][x] += 1

    def entferne_Werkzeug(self, x, y):
        if self.feld[y][x] != -1 and self.feld[y][x] != 0:
            self.feld[y][x] -= 1

