from tkinter import *
from threading import Thread
from time import sleep

class GUI(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.test = None

    def run(self):
        hauptfenster=Tk()
        hauptfenster.geometry("743x688")
        self.test = '1234'
        hauptfenster.mainloop()

g = GUI()
g.start()
while g.test is None:
    pass
print('Hello', g.test)
