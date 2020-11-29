'''
Created on 28.11.2020

@author: MD
'''
from Wechselrichter import Wechselrichter
from light.Cololight import PyCololight
import time
import logging


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


class Solarlight:
    
    def __init__(self):
        #print(sys.argv[1])
        self.wr1=Wechselrichter("192.168.0.156")
        #test
        self.wr1.getValue("Netzbezug")
        self.wr1.getValue("Einspeisung")
    
        #Establish cololight connection
        self.col = PyCololight("192.168.0.167")
        self.col.brightness=100  
        
        self.errorcnt = 0
    
    
    def setColorSimple(self, einspeisung):
        # Falls Einspeisung >=7000 -> 70% Warnung -> GelbBlau
        #
        # Falls Einspeisung >5000 GelbGrün
        # Falls Einspeisung >3000 Gelb
        #
        # Falls Einspeisung <100 GelbRot
        # Falls Netzbezug >100 Rot
        if einspeisung > 7000:
            self.col.brightness=100
            self.col.colour = [0xeb,0x5b,0x34]
        elif einspeisung > 6000:
            self.col.brightness=100
            self.col.colour = [0xeb,0xc6,0x34]
        elif einspeisung > 5000:
            self.col.brightness=100
            self.col.colour = [0xeb,0xd2,0x34]
        elif einspeisung > 4000:
            self.col.brightness=80
            self.col.colour = [0xeb,0xdf,0x34]
        elif einspeisung > 3000:
            self.col.brightness=70
            self.col.colour = [0xeb,0xef,0x34]
        elif einspeisung > 2000:
            self.col.brightness=60
            self.col.colour = [0xeb,0xff,0x34]
        elif einspeisung > 1000:
            self.col.brightness=60
            self.col.colour = [0xc3,0xeb,0x34]
        elif einspeisung > 1:
            self.col.brightness=60
            self.col.colour = [0xcc,0xeb,0x34]
        else:
            self.col.brightness=100
            self.col.colour = [0xeb,0x34,0xa1]
        
    
    def setColorMood(self, einspeisung, netzbezug):
        mode=6
        if einspeisung >= 7000:
            color = "Red"
            speed = 32
        elif einspeisung >= 6000: 
            speed = 28 + int((einspeisung-6000)/200)
            color = "Orange"
        elif einspeisung >= 4000: #4000-6000
            speed = 28 + int((einspeisung-4000)/400)
            color = "Yellow"
        elif einspeisung >= 2500:
            speed = 28 + int((einspeisung-2500)/250)
            color = "Green"
        elif einspeisung >= 1500:
            speed = 28 + int((einspeisung-1500)/200)
            color = "Grass"
        elif einspeisung >= 500: #500-1499
            speed = 28 + int((einspeisung-500)/200)
            color = "Gold"
        elif einspeisung >= 1: #1-500
            speed = 28 + int(einspeisung/100)
            color = "Azure"
        elif netzbezug <= 200: #0- -100
            speed = 24
            color = "Azure"
            mode=17
        elif netzbezug <= 1000: #0- -100
            speed = 25 + min(int((netzbezug/200)),7)
            color = "Pink"
            mode=17
        else:
            speed = 25 + min(int(((netzbezug-1000)/200)),7)
            color = "Red"
            mode=17
            
            
        
        oldhex = self.col._effects.get("Current",0)
        self.col.add_custom_effect("Current","Mood",color,speed,mode)
        newhex = self.col._effects.get("Current",0)
        if oldhex == newhex:
            print("Same color & speed, skip cololight cmd")
            return

        print(f"Set ColoLight {color} S:{speed} M:{mode}")
        self.col.effect = "Current"
        
    
    def runLoop(self):
        #en=-500
        netzbezug=0
        while True:
            try:
                einspeisung = self.wr1.getValue("Einspeisung")
                if einspeisung <= 1:
                    netzbezug = self.wr1.getValue("Netzbezug")
            #    einspeisung = en
            #   netzbezug=en*-1
            #    en=en+200
                print(f"Calculate Color Mode for Einsp:{einspeisung} Netz:{netzbezug}")
                self.setColorMood(einspeisung, netzbezug)
                self.errorcnt = 0 # reset error count
                time.sleep(5)
            except Exception as e:
                self.handleerror(e)
    
    
    def handleerror(self, e):
        #Set color to white and flash
        self.errorcnt = self.errorcnt +1
        print(f"Exception: {e} {self.errorcnt}")
        self.col.add_custom_effect("Current","Flash","White",29,17)
        time.sleep(self.errorcnt*60)
        

if __name__ == "__main__":
    sl = Solarlight()
    sl.runLoop()
    
    
    