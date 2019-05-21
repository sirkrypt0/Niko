# -*- coding: cp1252 -*-

from Tkinter import *
from welt import *
from dateiDialog import *
from gui import *
import tkMessageBox

from niko import RESOURCE_PFAD

class Editor(GuiLayout):
    def __init__(self):

        self.welt = Welt()

        GuiLayout.__init__(self, self.welt)
        
        self.hauptfenster.protocol("WM_DELETE_WINDOW", self.close)

        self.title = "Niko-Editor"

        #Datei
        self.standardDateiPfad = os.getcwd() + "\\NeueWelt.welt"
        self.dateipfad = self.standardDateiPfad
        self.gespeichert = False
        self.neu = True

        self.titelAktualisieren()

        #Bilder
        self.mausBild = PhotoImage(file=RESOURCE_PFAD+"maus.gif")
        
        #GUI Elemente

        self.welt_CNV.bind("<1>",self.toggleMauerEvent)
        self.welt_CNV.bind("<2>",self.werkzeugSetzenEvent)
        self.welt_CNV.bind("<3>",self.werkzeugEntfernenEvent)

        self.titel_LBL = Label (self.leiste_FRM, text="Der Welteditor", bg=self.leistenHintergrund)
        self.titel_LBL.place(x=10, y=20)

        self.loescheAlles_BTN = Button(self.leiste_FRM, text="Alles löschen", command=self.loescheAlles)
        self.loescheAlles_BTN.place(x=10, y=40)

        self.bild_LBL = Label (self.leiste_FRM, image=self.mausBild)
        self.bild_LBL.place(x=0, y=220)

        self.untertitel_LBL = Label (self.leiste_FRM, text="NikoED, der RoboCop", bg=self.leistenHintergrund)
        self.untertitel_LBL.place(x=10, y=520)

        #Menu
        self.menubar=Menu(self.hauptfenster)
        self.menu=Menu(self.menubar)
        
        self.hauptfenster.config(menu=self.menubar)
        
        self.menubar.add_cascade(label="Datei", menu=self.menu)
        
        self.menu.add_command(label="Neu", command=self.neu)

        #Speichern
        self.menu.add_command(label="Speichern", command=lambda:self.weltSpeichern(0))
        self.hauptfenster.bind("<Control-s>", lambda event:self.weltSpeichern(0))

        #Speichern als
        self.menu.add_command(label="Speichern als", command=lambda:self.weltSpeichern(1))
        self.hauptfenster.bind("<Control-S>", lambda event:self.weltSpeichern(1))

        self.menu.add_command(label="Öffnen", command=self.weltLaden)

        self.hauptfenster.mainloop()

    def close(self):
        if not self.gespeichert:
            speichern = tkMessageBox.askquestion("Datei speichern?", "Datei wurde nicht gespeichert!\nJetzt speichern?", icon="warning")
            if speichern == "yes":
                self.weltSpeichern()
        
        self.hauptfenster.quit()
        self.hauptfenster.destroy()

    def titelAktualisieren(self):
        dateiname = self.dateipfad.split("\\")[-1]
        
        if self.gespeichert:
            self.hauptfenster.title(self.title + " - %s - %s" %(dateiname, self.dateipfad))
        else:
            self.hauptfenster.title(self.title + " - *%s - %s" %(dateiname, self.dateipfad))

    def loescheAlles(self):
        self.welt = Welt()
        if self.welt_CNV.find_withtag('bild'):
            self.welt_CNV.delete("bild")

    def koordinaten(self,event):
        x = event.x/self.welt_CNV.feldgroesse
        if x > 13: x = 13
        
        y = event.y/self.welt_CNV.feldgroesse
        if y > 13: y = 13
        
        return (x,y)

    def speicherzustandAktualisieren(self, zustand):
        self.gespeichert = zustand
        self.titelAktualisieren()

    def aktualisieren(self):
        #Änderung erkennen
        if self.gespeichert:
            self.speicherzustandAktualisieren(False)
            
        self.welt_CNV.aktualisiere()
        
    def toggleMauerEvent(self,event):
        (x,y) = self.koordinaten(event)
        if self.welt.feld_leer(x,y):
            self.welt.setze_Mauer(x,y)
        elif self.welt.mauerVorhanden(x,y):
            self.welt.entferne_Mauer(x,y)
        self.aktualisieren()
            
    def werkzeugSetzenEvent(self,event):
        (x,y) = self.koordinaten(event)
        if not self.welt.mauerVorhanden(x,y):
            self.welt.setze_Werkzeug(x,y)
        self.aktualisieren()

    def werkzeugEntfernenEvent(self, event):
        (x,y) = self.koordinaten(event)
        if self.welt.zaehle_Werkzeug(x,y) >= 0:
            self.welt.entferne_Werkzeug(x,y)
        self.aktualisieren()

    def neu(self):
        self.dateipfad = self.standardDateiPfad
        self.loescheAlles()
        self.speicherzustandAktualisieren(False)
        self.neu = True

    #mode = 0 -> Speichern; mode = 1 -> Speichern als
    def weltSpeichern(self, mode=0):
        #Datei nicht vorhanden oder Speichern als
        if self.neu or mode == 1:
            dialog = SpeichernDialog(self.welt.feld, self.dateipfad, 0)
            
            if dialog.gespeichert:
                self.dateipfad = dialog.datei
                self.speicherzustandAktualisieren(True)
                self.neu = False
                
        else:
            dialog = SpeichernDialog(self.welt.feld, self.dateipfad, 1)
            
            self.speicherzustandAktualisieren(True)
        

    def weltLaden(self):
        dialog = OeffnenDialog()
        
        if dialog.geoeffnet:
            self.welt.feld = dialog.welt
            self.dateipfad = dialog.datei
            
            self.speicherzustandAktualisieren(True)
            self.aktualisieren()

if __name__=="__main__":
    gui = Editor()
        
