#wird aufgerufen wenn Befehl gegeben wurde
#Methode für jede Pumpe oder eine für alle? Anhand der Pins unterscheiden?
#starte die Pumpe
import pyfirmata
import time
import Cocktail
import threading

board = pyfirmata.Arduino('/dev/tty.usbmodem101')

ingredient = {'rum':2, 'gin':4, 'limette':5, 'wasser':6, 'sirup':7}

def stopPump(ing):
    board.digital[ing].write(0)

def start(ingridient, ml):
    board.digital[ingridient].write(1)
    threading.Timer(ml, stopPump, [ingridient]).start()
    #threading.Timer(ml, abbruch).start()
    # das hat nicht funktiniert??
    #time.sleep(ml)
    #board.digital[ingridient].write(0)

def mixIT(cocktail):
    print(cocktail.inhalt.items)
    for ing, ml in cocktail.inhalt.items():
        if ml != 0:
            # start(ingredient.get(ing), ml)
            threading.Thread(target=start, args=(ingredient.get(ing), ml)).start()

def abbruch():
    board.digital[2].write(0)
    board.digital[4].write(0)
    board.digital[5].write(0)
    board.digital[6].write(0)
    board.digital[7].write(0)

    