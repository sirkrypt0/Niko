from .gui import *
from time import *
from .welt import *

class Roboter:
    welt = None
    guiLayout = None
    def __init__(self, weltdatei=None, verzoegerung=0.1):

        self.verzoegerung = verzoegerung
        
        if Roboter.welt is None:
            if not weltdatei:
                Roboter.welt = Welt()
            else:
                Roboter.welt = Welt(weltdatei)
        
        self.pos_x = self.pos_y = self.welt.dimension-1
        self.ausrichtung = 0
        self.vorrat = 200
        self.lager = 0

        if Roboter.guiLayout is None:
            Roboter.guiLayout = GuiThreaded(Roboter.welt)
            Roboter.guiLayout.start()
            while Roboter.guiLayout.welt_CNV is None: # warte bis thread gestartet ist
                pass
        
        self.interface = Roboter.guiLayout
        self.interface.aktualisiere(self)

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

        sleep(self.verzoegerung)
        self.interface.aktualisiere(self)

    def links(self):
        self.ausrichtung = (self.ausrichtung + 1) % 4

        sleep(self.verzoegerung)
        self.interface.aktualisiere(self)

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
        
        sleep(self.verzoegerung)
        self.interface.aktualisiere(self)
        
    def gib(self):
        self.welt.setze_Werkzeug(self.pos_x, self.pos_y)
        self.vorrat -= 1
        
        sleep(self.verzoegerung)
        self.interface.aktualisiere(self)
