from Tkinter import *
import tkFileDialog
from roboter import *

from niko import RESOURCE_PFAD

class Ti:
    def __init__(self):

        self.roboter = Roboter(None, 0)
        
        self.button_FRM = self.roboter.guiLayout.leiste_FRM
        
        #Buttons
        self.vor_BTN=Button(self.button_FRM,bg="pink",text="vor",command=self.guivor)
        self.vor_BTN.place(x=10,y=10,width=120,height=40)
        
        self.links_BTN=Button(self.button_FRM,bg="pink",text="links",command=self.guilinks)
        self.links_BTN.place(x=10,y=50,width=120,height=40)

        self.gib_BTN=Button(self.button_FRM,bg="pink",text="gib",command=self.guigib)
        self.gib_BTN.place(x=10,y=210,width=120,height=40)
        
        self.nimm_BTN=Button(self.button_FRM,bg="pink",text="nimm",command=self.guinimm)
        self.nimm_BTN.place(x=10,y=250,width=120,height=40)
        
        #Aufnahmeknopf
        self.record = PhotoImage(file=RESOURCE_PFAD+"record.gif")

        self.stop = PhotoImage(file=RESOURCE_PFAD+"stop.gif")
        
        self.record_BTN=Button(self.button_FRM,command=self.recordstart,image=self.record)
        self.record_BTN.place(x=25,y=329,width=90,height=90)

        self.roboterBild = PhotoImage(file=RESOURCE_PFAD+"robi_0.gif")

        self.roboter.interface.aktualisiere(self.roboter)

        self.recording=False

        self.log=[]
        
    def guirechts(self):
        if self.recording:
            self.log.append("roboter.rechts()")
        self.roboter.rechts()
        
    def guilinks(self):
        if self.recording:
            self.log.append("roboter.links()")
        self.roboter.links()

    def guivor(self):
        if self.recording:
            self.log.append("roboter.vor()") #Aufpassen:wenn das feld zuende ist dokumentiert er trotzdem das weiterlaufen!
        self.roboter.vor()
        
    def guinimm(self):
        if self.recording:
            self.log.append("roboter.nimm()")
        self.roboter.nimm()
        
    def guigib(self):
        if self.recording:
            self.log.append("roboter.gib()")
        self.roboter.gib()

        
    def recordstart(self):
        self.record_BTN.configure(text="Aufnahme stoppen",command=self.recordstop,image=self.stop)
        self.log=["from niko.roboter import *","roboter=Roboter('test.welt', 0.1)"]
        self.recording=True
        
    def recordstop(self):
        self.record_BTN.configure(text="Aufnahme starten",command=self.recordstart,image=self.record)
        self.recording=False
        
        log_out=open(tkFileDialog.asksaveasfilename(defaultextension=".py",initialfile="Log",title="Robomoves als Log speichern"),"w")
        for befehl in self.log:
            log_out.write(befehl+"\n")
        log_out.close()


if __name__=="__main__":
    ti = Ti()
