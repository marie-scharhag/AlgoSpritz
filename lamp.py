import pyfirmata
import time
import threading

board = pyfirmata.Arduino('/dev/tty.usbmodem142401')

RED_LED = 11
GREEN_LED = 12
BLUE_LED = 13

def party():
    while True:
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

def noParty():
    board.digital[RED_LED].write(1)
    board.digital[GREEN_LED].write(1)
    board.digital[BLUE_LED].write(1)

def anschalten():
    board.digital[BLUE_LED].write(1)
    board.digital[RED_LED].write(1)
    for i in range(3):
        board.digital[GREEN_LED].write(1)
        time.sleep(0.5)
        board.digital[GREEN_LED].write(0)
        time.sleep(0.5)
    board.digital[GREEN_LED].write(1)


def ausschalten():
    board.digital[GREEN_LED].write(1)
    board.digital[BLUE_LED].write(1)
    for i in range(3):
        board.digital[RED_LED].write(1)
        time.sleep(0.5)
        board.digital[RED_LED].write(0)
        time.sleep(0.5)
    board.digital[RED_LED].write(1)

