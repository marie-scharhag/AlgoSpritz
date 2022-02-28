#wird aufgerufen wenn Befehl gegeben wurde
#Methode für jede Pumpe oder eine für alle? Anhand der Pins unterscheiden?
#starte die Pumpe
import pyfirmata
import time
import Cocktail

board = pyfirmata.Arduino('/dev/tty.usbmodem1101')

rum = 1 #nummer vom PIN
gin = 4
limette = 5
wasser = 6
sirup = 7 

def mixIT(cocktail):
    for ingridient, ml in cocktail.inhalt.items():
        if ml != 0:
            start(ingridient, ml)

def start(ingridient, ml):
    board.digital[ingridient].write(1)
    time.sleep(ml)
    board.digital[ingridient].write(0)
