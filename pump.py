#wird aufgerufen wenn Befehl gegeben wurde
#Methode für jede Pumpe oder eine für alle? Anhand der Pins unterscheiden?
#starte die Pumpe
import pyfirmata
import time
import Cocktail

board = pyfirmata.Arduino('/dev/tty.usbmodem142401')

ingredient = {'rum':2, 'gin':4, 'limette':5, 'wasser':6, 'sirup':7}

def mixIT(cocktail):
    print(cocktail.inhalt.items)
    for ing, ml in cocktail.inhalt.items():
        if ml != 0:
            start(ingredient.get(ing), ml)

def start(ingridient, ml):
    board.digital[ingridient].write(1)
    time.sleep(ml)
    board.digital[ingridient].write(0)
