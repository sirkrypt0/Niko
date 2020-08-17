from .gui import *
from time import *
from .welt import *

class Roboter:
    welt = None
    guiLayout = None
    anzahl = 0
    def __init__(self, weltdatei=None, verzoegerung=0.1, weltobjekt=None, name=None, gui=None):

        self.name = f"roboter{Roboter.anzahl}" if name is None else name
        Roboter.anzahl += 1
        self.verzoegerung = verzoegerung
        if Roboter.welt is None:
            if weltobjekt is not None:
                Roboter.welt = weltobjekt
            elif weltdatei is None:
                Roboter.welt = Welt()
            else:
                Roboter.welt = Welt(weltdatei)
        
        self.pos_x = self.pos_y = self.welt.dimension-1
        self.ausrichtung = 0
        self.vorrat = 200
        self.lager = 0

        if Roboter.guiLayout is None and gui is None:
            Roboter.guiLayout = GuiThreaded(Roboter.welt)
            Roboter.guiLayout.start()
            while Roboter.guiLayout.welt_CNV is None: # warte bis thread gestartet ist
                pass
        
        self.interface = Roboter.guiLayout if gui is None else gui
        self.interface.roboterAktualisieren(self)

    def positionAktualisieren(self):
        sleep(self.verzoegerung)
        self.interface.roboterAktualisieren(self)

    def vor(self):
        if self.ausrichtung == 0:
            if self.pos_y != 0:
                self.pos_y -= 1
        elif self.ausrichtung == 1:
            if self.pos_x != 0 :
                self.pos_x -= 1
        elif self.ausrichtung == 2:
            if self.pos_y != self.welt.dimension-1:
                self.pos_y += 1
        elif self.ausrichtung == 3:
            if self.pos_x != self.welt.dimension-1:
                self.pos_x += 1
        self.positionAktualisieren()   

    def links(self):
        self.ausrichtung = (self.ausrichtung + 1) % 4
        self.positionAktualisieren()

    def vorne_frei(self):
        if self.ausrichtung == 0:
            if self.pos_y > 0 and not self.welt.mauerVorhanden(self.pos_x,self.pos_y-1):
                return 1
            else:
                return 0
        elif self.ausrichtung == 1:
            if self.pos_x > 0 and not self.welt.mauerVorhanden(self.pos_x-1,self.pos_y):
                return 1
            else:
                return 0
        elif self.ausrichtung == 2:
            if self.pos_y < self.welt.dimension-1 and not self.welt.mauerVorhanden(self.pos_x,self.pos_y+1):
                return 1
            else:
                return 0
        elif self.ausrichtung == 3:
            if self.pos_x < self.welt.dimension-1 and not self.welt.mauerVorhanden(self.pos_x+1,self.pos_y):
                return 1
            else:
                return 0

    def feld_leer(self):
        return self.welt.feld_leer(self.pos_x, self.pos_y)
        
    def nimm(self):
        self.welt.entferne_Werkzeug(self.pos_x, self.pos_y)
        self.lager += 1
        self.interface.werkzeugeAktualisieren()
        
    def gib(self):
        self.welt.setze_Werkzeug(self.pos_x, self.pos_y)
        self.vorrat -= 1
        self.interface.werkzeugeAktualisieren()
