from niko import *
rob = Roboter("test.welt")
for i in range(9):
    rob.gib()
    rob.vor()
rob.links()
rob.links()
for i in range(9):
    rob.vor()
    rob.nimm()