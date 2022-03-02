import pyfirmata
import time
import threading

board = pyfirmata.Arduino('/dev/tty.usbmodem101')

RED_LED = 11
GREEN_LED = 12
BLUE_LED = 13

pp = False

def startPP():
    global pp
    pp = True

def party():
    global pp
    if pp:
        board.digital[GREEN_LED].write(0)
        board.digital[BLUE_LED].write(0)
        time.sleep(1)
        board.digital[GREEN_LED].write(1)
        board.digital[RED_LED].write(0)
        time.sleep(1)
        board.digital[BLUE_LED].write(1)
        board.digital[GREEN_LED].write(0)
        time.sleep(1)
        board.digital[RED_LED].write(1)
        party()

def lightOn():
    global pp
    pp = False
    board.digital[RED_LED].write(0)
    board.digital[GREEN_LED].write(0)
    board.digital[BLUE_LED].write(0)

def lightOff():
    global pp
    pp = False
    board.digital[RED_LED].write(1)
    board.digital[GREEN_LED].write(1)
    board.digital[BLUE_LED].write(1)

def anschalten():
    global pp
    pp = False
    board.digital[BLUE_LED].write(1)
    board.digital[RED_LED].write(1)
    for i in range(3):
        board.digital[GREEN_LED].write(1)
        time.sleep(0.5)
        board.digital[GREEN_LED].write(0)
        time.sleep(0.5)
    lightOff()


def ausschalten():
    global pp
    pp = False
    board.digital[GREEN_LED].write(1)
    board.digital[BLUE_LED].write(1)
    for i in range(3):
        board.digital[RED_LED].write(1)
        time.sleep(0.5)
        board.digital[RED_LED].write(0)
        time.sleep(0.5)
    lightOff()

