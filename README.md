# SolarLight
Use ColoLight to visualize the power generation of SMA inverter 



To get started:

1) Clone git repo
2) Edit Solarlight.py and replace IP address for SMA inverter and Cololight
3) The SMA register numbers are for STP10k inverters, other models might need different register numbers (in Wechselrichter.py)
4) Run Solarlight.py and enjoy the colors



        **Grid feed-in (W) colors (Mood, mode 6):**
        
        #>7000W Red
        #6000-7000 Orange
        #4000-6000 yellow
        #2500-4000 Green
        #1500-2500 Grass       
        #500-1499 Gold
        #1-500W Azure
        
        ** Grid supply (W) colors (Mood, mode 17):**
        0-200W Azure
        200-1000W Pink
        >1000W Red
        
        
        
Thanks to BazaJayGee66 for the Cololight python class ( Github BazaJayGee66 / homeassistant_cololight)
        
