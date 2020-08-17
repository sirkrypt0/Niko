# -*- coding: cp1252 -*-
from tkinter import *
import os

from .util import resource_path

class DateiDialog():

    def __init__(self):
        self.toplevel = Toplevel()
        self.toplevel.geometry("400x300")
        self.toplevel.title("Dateiexplorer")

        self.toplevel.focus_force()
        self.toplevel.protocol("WM_DELETE_WINDOW", self.close)

        self.welt = []
        self.datei = ""

        self.verzeichnis_ETY = Entry(self.toplevel, width=50)
        self.verzeichnis_ETY.place(x=35, y=14)
        self.verzeichnis_ETY.insert(0, os.getcwd())

        self.verzeichnis_ETY.bind('<Return>', self.verzeichnisWechselnETY)

        self.zurueck_bild = PhotoImage(file=resource_path("zurueckKnopf.gif"))
        
        self.zurueck_BTN = Button(self.toplevel, image=self.zurueck_bild, command=lambda:self.verzeichnisWechseln(None,".."))
        self.zurueck_BTN.place(x=5, y=10)

        # Verzeichnis anzeigen

        self.verzeichnis_FRM = Frame(self.toplevel)
        self.verzeichnis_FRM.place(x=35, y=40)
        
        self.scrollbar = Scrollbar(self.verzeichnis_FRM)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        self.liste = Listbox(self.verzeichnis_FRM, selectmode=SINGLE, width=50)
        self.liste.pack()

        self.liste.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.liste.yview)

        self.liste.bind('<Double-Button-1>', self.verzeichnisWechseln)
        self.liste.bind('<Return>', self.verzeichnisWechseln)

        self.listboxUpdaten()

    # Sicherstellen dass auch der mainloop beendet wird, damit das Hauptfenster
    # korrekt weiterlaufen kann
    def close(self):
        self.toplevel.quit()
        self.toplevel.destroy()

    def filtern(self, liste, endung):
        listeNeu = []
        for datei in liste:

            # Verzeichnisse außer Acht lassen, aber mit in Liste aufnehmen
            if not (os.path.isfile(os.getcwd()+"/"+datei)):
                listeNeu.append(datei)
                continue
            
            end = datei.split(".")[-1]
            if end == endung:
                listeNeu.append(datei)
                
        return listeNeu

    def listboxUpdaten(self):
        self.verzeichnis_ETY.delete(0, END)
        self.verzeichnis_ETY.insert(0, os.getcwd())
        
        inhalt = os.listdir(os.getcwd())
        inhalt = self.filtern(inhalt, "welt")
        
        self.liste.delete(0, END)
        self.liste.insert(END, "..")
        for i in inhalt:
            self.liste.insert(END,i)

    def verzeichnisWechseln(self, event=None, pfad=None):
        curSel = self.liste.curselection()
        if pfad:
            if os.path.isdir(pfad):
                os.chdir(pfad)
                self.listboxUpdaten()
        elif curSel:
            neuVerz = self.liste.get(curSel[0])
            if os.path.isdir(neuVerz):
                os.chdir(neuVerz)
                self.listboxUpdaten()

    def verzeichnisWechselnETY(self, event=None):
        neuVerz = self.verzeichnis_ETY.get()
        if neuVerz:
            if os.path.isdir(neuVerz):
                os.chdir(neuVerz)
                self.listboxUpdaten()

class SpeichernDialog(DateiDialog):
    
    def __init__(self, welt, dateipfad, mode=0):
        DateiDialog.__init__(self)

        self.welt = welt
        self.datei = dateipfad
        
        self.gespeichert = False

        self.liste.bind("<<ListboxSelect>>", self.onListboxSelect)
        
        #Neue Datei
            
        self.neueDatei_ETY = Entry(self.toplevel, width= 33)
        self.neueDatei_ETY.place(x=35, y=210)
        self.neueDatei_ETY.insert(0,os.path.basename(self.datei))        

        self.neueDatei_BTN = Button(self.toplevel, text="Datei speichern", font="Calibri 9", command=self.neueDatei)
        self.neueDatei_BTN.place(x=243, y=209, height=20)

        #Neues Verzeichnis

        self.verzeichnis_bild = PhotoImage(file=resource_path("verzeichnisAnlegen.gif"))
                                           
        self.neuesVerzeichnis_BTN = Button(self.toplevel, image=self.verzeichnis_bild, command=self.neuesVerzeichnis)
        self.neuesVerzeichnis_BTN.place(x=343, y=10)
        
        if mode == 1:
            self.neueDatei(mode)
            self.toplevel.destroy()
        else:
            self.toplevel.mainloop()

    def onListboxSelect(self, event):
        selection = self.liste.get(self.liste.curselection())

        # Entry nur bei Dateien ausfuellen
        if os.path.isfile(os.path.join(os.getcwd(), selection)):
            self.neueDatei_ETY.delete(0, END)
            self.neueDatei_ETY.insert(0, selection)

    def neueDatei(self, mode=0):
        if mode == 0:
            name = self.neueDatei_ETY.get()#+".welt"
        else:
            name = self.datei
            
        try:
            datei = open(name, "w")
            
            # Welt in Datei speichern
            for elemY in self.welt:
                zeile = ""
                for elemX in elemY:
                    zeile += str(elemX) + " "
                zeile = zeile.rstrip()
                zeile += "\n"
                datei.write(zeile)

            #Dateipfad zum neu öffnen speichern
            self.datei = os.path.join(os.getcwd(), name)
            self.gespeichert = True
            
            datei.close()
        except:
            pass

        if mode == 0:
            self.toplevel.quit()
            self.toplevel.destroy()

    def neuesVerzeichnis(self):
        name = self.neuesVerzeichnis_ETY.get()
        try:
            os.mkdir(name)
        except:
            #Errormeldung anzeigen
            pass
        
        self.listboxUpdaten()

class OeffnenDialog(DateiDialog):
    def __init__(self):
        DateiDialog.__init__(self)

        self.geoeffnet = False
        
        #Datei oeffnen

        self.dateiOeffnen_BTN = Button(self.toplevel, text="Datei öffnen", command=self.dateiOeffnen)
        self.dateiOeffnen_BTN.place(x=150,y=209)

        self.toplevel.mainloop()
        
    def dateiOeffnen(self):
        curSel = self.liste.curselection()
        if curSel:
            name = self.liste.get(curSel[0])
            if os.path.isfile(name):
                datei = open(name, "r")
                inhalt = datei.readlines()
                welt = []
                for zeile in inhalt:
                    zeile = zeile.strip()
                    zeile = zeile.split(" ")
                    for i in range(len(zeile)):
                        zeile[i] = int(zeile[i])
                    welt.append(zeile)
                self.welt = welt

                #Dateinamen zum neu öffnen speichern
                self.datei = os.path.join(os.getcwd(), name)

                self.geoeffnet = True
                
                datei.close()
                
                self.toplevel.quit()
                self.toplevel.destroy()
