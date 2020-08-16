from tkinter import *
from threading import Thread

from .util import resource_path

class GuiLayout(Thread):
    welt_CNV = None
    def __init__(self, welt):
        Thread.__init__(self)
        self.welt = welt
        self.hauptfenster=Tk()
        self.hauptfenster.geometry("743x688")

        self.feldHintergrund = "white"
        self.leistenHintergrund = "#BBBBBB"
        
        self.welt_CNV = WeltCanvas(self.hauptfenster, self.feldHintergrund, self.welt)

        self.leiste_FRM = BasisFrame(self.hauptfenster, self.leistenHintergrund)

    def run(self):
        self.hauptfenster.mainloop()

class WeltCanvas(Canvas):
    def __init__(self, hauptfenster, hintergrund, welt):
        Canvas.__init__(self, hauptfenster, highlightbackground="black", highlightthickness=1, bg=hintergrund)

        self.welt = welt
        
        self.groesse = 588
        self.feldgroesse = self.groesse/self.welt.dimension
        
        #Weltfeld(Canvas)
        self.place(x=5,y=50,width=self.groesse,height=self.groesse)
        
        #Linien Zeichnen
        for x in range(1,self.welt.dimension):
            self.create_line(x*self.feldgroesse,0,x*self.feldgroesse,self.groesse)
        for y in range(1,self.welt.dimension):
            self.create_line(0,y*self.feldgroesse,self.groesse,y*self.feldgroesse)

        self.mauerBild = PhotoImage(file=resource_path("mauer.gif"))
        self.hammerBild = PhotoImage(file=resource_path("hammer.gif"))
        
        self.roboterBildOben = PhotoImage(file=resource_path("robi_0.gif"))
        self.roboterBildLinks = PhotoImage(file=resource_path("robi_1.gif"))
        self.roboterBildUnten = PhotoImage(file=resource_path("robi_2.gif"))
        self.roboterBildRechts = PhotoImage(file=resource_path("robi_3.gif"))
        
        self.aktualisiere()
    
    def rasterZeichnen(self):
        lineOffset = 2
        self.welt_CNV.create_line(lineOffset, lineOffset, self.grosse, lineOffset, fill="blue")
        self.welt_CNV.create_line(lineOffset, lineOffset, lineOffset, self.grosse, fill="blue")
        self.welt_CNV.create_line(0, self.grosse, self.grosse+1, self.grosse, fill="blue")
        self.welt_CNV.create_line(self.grosse, 0, self.grosse, self.grosse, fill="blue")
        for i in range(1,self.welt.dimension):
            self.welt_CNV.create_line(0,i*self.feldgrosse, self.grosse,i*self.feldgrosse,fill="blue")
        for j in range(1,self.welt.dimension):
            self.welt_CNV.create_line(j*self.feldgrosse,0, j*self.feldgrosse,self.grosse, fill="blue")
            
    def aktualisiere(self, roboter=None):
        if self.find_withtag('bild'):
            self.delete("bild")
        for y in range(self.welt.dimension):
            for x in range(self.welt.dimension):
                xp = x*self.feldgroesse + self.feldgroesse*0.5
                yp = y*self.feldgroesse + self.feldgroesse*0.5

                if self.welt.mauerVorhanden(x,y):
                    self.create_image(xp,yp, anchor=CENTER, image=self.mauerBild, tags=("bild"))
                if self.welt.zaehle_Werkzeug(x,y) > 0:
                    self.create_image(xp,yp, anchor=CENTER, image=self.hammerBild, tags=("bild"))

        if roboter:
            if self.find_withtag("roboter"):
                self.delete("roboter")

            robX = roboter.pos_x * self.feldgroesse + self.feldgroesse * 0.5
            robY = roboter.pos_y * self.feldgroesse + self.feldgroesse * 0.5

            if roboter.ausrichtung == 0:
                image = self.roboterBildOben
            if roboter.ausrichtung == 1:
                image = self.roboterBildLinks
            if roboter.ausrichtung == 2:
                image = self.roboterBildUnten
            if roboter.ausrichtung == 3:
                image = self.roboterBildRechts
                
            self.create_image(robX, robY, anchor=CENTER, image=image, tags=("roboter"))

class BasisFrame(Frame):
    def __init__(self,hauptfenster,hintergrund):
        #Frame           
        Frame.__init__(self, hauptfenster, bg=hintergrund, bd=2)
        self.place(x=598,y=50,width=140,height=588)
