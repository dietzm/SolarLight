'''
Created on 28.11.2020

@author: MD mail@dietzm.de
'''
from light.Cololight import PyCololight
import time

if __name__ == '__main__':
    print("Hello")
    col = PyCololight("192.168.0.167")
    
    col.brightness=100
    col.colour = [0xff,0x00,0xff]

    print(col.effects)
    col.effect = "The Circus"
    
    print("Custom")
    time.sleep(1)
    
    
    for i in range(1,100):
        speed=i%6+26
        col.add_custom_effect("Test","Mood","Green",speed,6)
        col.effect = "Test"
        time.sleep(10);
        print(speed)
    