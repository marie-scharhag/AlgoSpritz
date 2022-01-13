#wird aufgerufen wenn Befehl gegeben wurde
#Methode für jede Pumpe oder eine für alle? Anhand der Pins unterscheiden?
#starte die Pumpe
import pyfirmata
import time

board = pyfirmata.Arduino('/dev/tty.usbmodem11301')

while True:
    board.digital[13].write(1)
    time.sleep(10)
    board.digital[13].write(0)
    time.sleep(10)
