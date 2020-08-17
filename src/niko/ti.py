from tkinter import *
import tkinter.filedialog
from .roboter import *
from .gui import *

from .util import resource_path

class Ti(GuiLayout):
    def __init__(self):
        GuiLayout.__init__(self, Welt())
        self.roboter = Roboter(weltobjekt=self.welt, verzoegerung=0, gui = self)

        self.hauptfenster.title("Niko - Teaching interactive")
        
        #Buttons
        self.vor_BTN=Button(self.leiste_FRM,bg="pink",text="vor",command=self.guivor)
        self.vor_BTN.place(x=10,y=10,width=120,height=40)
        
        self.links_BTN=Button(self.leiste_FRM,bg="pink",text="links",command=self.guilinks)
        self.links_BTN.place(x=10,y=50,width=120,height=40)

        self.gib_BTN=Button(self.leiste_FRM,bg="pink",text="gib",command=self.guigib)
        self.gib_BTN.place(x=10,y=210,width=120,height=40)
        
        self.nimm_BTN=Button(self.leiste_FRM,bg="pink",text="nimm",command=self.guinimm)
        self.nimm_BTN.place(x=10,y=250,width=120,height=40)
        
        #Aufnahmeknopf
        self.record = PhotoImage(file=resource_path("record.gif"))

        self.stop = PhotoImage(file=resource_path("stop.gif"))
        
        self.record_BTN=Button(self.leiste_FRM,command=self.recordstart,image=self.record)
        self.record_BTN.place(x=25,y=329,width=90,height=90)

        self.roboterBild = PhotoImage(file=resource_path("robi_0.gif"))

        self.roboter.positionAktualisieren()

        self.recording=False

        self.log=[]

        self.hauptfenster.mainloop()
        
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
        
        log_out=open(tkinter.filedialog.asksaveasfilename(defaultextension=".py",initialfile="Log",title="Robomoves als Log speichern"),"w")
        for befehl in self.log:
            log_out.write(befehl+"\n")
        log_out.close()
