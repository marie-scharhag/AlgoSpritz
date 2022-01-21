#wird aufgerufen wenn Befehl gegeben wurde
#Methode für jede Pumpe oder eine für alle? Anhand der Pins unterscheiden?
#starte die Pumpe
import pyfirmata
import time

board = pyfirmata.Arduino('/dev/tty.usbmodem1101')

syrup = 5 #nummer vom PIN
gin = 4
water = 3
limejuice = 12
rum = 13 

#unsere cocktails mit zutat:ml in sekunden
caipi = {rum:10, limejuice:3} #, water:5}
mojito = {rum:10, limejuice:10, water:10, syrup:10}
ginsour = {limejuice:10, water:10, gin:10, syrup:10}

def mixIT(cocktail):
    if cocktail == "caipirinha":
        for ingridient, ml in caipi.items():
            start(ingridient, ml)
    if cocktail == "mojito":
        for ingridient, ml in mojito.items():
            start(ingridient, ml)
    if cocktail == "gin sour":
        for ingridient, ml in ginsour.items():
            start(ingridient, ml)

def start(ingridient, ml):
    board.digital[ingridient].write(1)
    time.sleep(ml)
    board.digital[ingridient].write(0)
