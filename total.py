from distutils.command.config import config
import speech_recognition as sr
import time
#import pump
import Cocktail
import pyttsx3
import pygame
import threading
import sys
import os
from random import randint

#to do:
#Musik auschalten: erledigt 
#abbruch musik: erledigt
#selbstauschalten hinweis: erledigt
#auschalten befehlen: erledigt
#vorherigen cocktail auswählen: erledigt
#beleidigungn: erledigt
#überraschungscocktail: erledigt 
#was hast du für cocktails?: erledigt
#was wenn cocktail gemischt wird, und neuer bestellt wird: erledigt
#alkohol nicht mehr verfügbar: machen wir nicht
#lange Zeit keine Interaktion mehr
#abbruch pumpen


#languageID bei Sprachausgabe 0 bei Windows und 4 bei Mac
language = 4

noCocktail =['Cuba Libre','Gin Tonic','Moscow Mule', 'Negroni', 'Pina Colada', 'Tequila Sunrise','Cuba Libre','Zombie']
mehr = ['zwei','2','drei','3', 'mal','vier','4','und','2 x']
abbruch = ['abbruch','stopp', 'halt','abbrechen','nein']
vorherigen = ['auch', 'gleichen', 'letzten', 'vorherigen','selben']
befehl =['mix','mach','mache','hätte','nehme','nehm','will','möchte','gib', 'ein', 'einen']
insult = ['fyou', 'a*', 'f*', 'maul', 'schnauze', 'h*']
musicoff = ['off','aus']
musicon = ['an','on']
musicname = ['music', 'musik']
algooff = ['ausschalten', 'vorbei']
surprise = ['überrasch', 'überraschung', 'egal', 'random', 'zufälligen', 'zufällig']
suggestion = ['was', 'welche', 'cocktails', 'vorschläge']
dicti = {"speech":"","lastCocktail":"", "noCocktail": False}

#music abspielen ja oder nein
music = True
#cocktail wird gemischt ja oder nein
cockInProgress = False

def bekannt(cocktail):
    for c in Cocktail.cocktails:
        if cocktail in c.name:
            cock = c
    text = "Okay, ein "+cocktail+" wird jetzt gemixt!" 
    print(text)
    mainSpeaking(text)
    playSong(cock)
    threading.Timer(cock.pumpZeit(), changecock).start()
    #pump.mixIT(cock)

def changecock():
    global cockInProgress
    if cockInProgress:
        cockInProgress = False
    else: 
        cockInProgress = True

def unbekannt(cocktail):
    text = "Sorry not sorry, das kann ich leider noch nicht zubereiten. "+cocktail
    print(">>>"+text) 
    mainSpeaking(text)
    wunsch()

def abbrechen():
    text = "Ok ok ich hör ja schon auf"
    #musik und pumpen abbrechen
    print(">>>"+text)
    if pygame.mixer.get_init():
        pygame.mixer.music.pause()
    #pump.abbruch()
    changecock()
    mainSpeaking(text)

def turnmusic():
    global music 
    if music: 
        music = False
        if not pygame.mixer.get_init():
            pygame.mixer.music.pause()
    else:
        music = True
 

def unverstaendlich():
    if cockInProgress:
        text = "Gerade wird ein spritziges Getränk zubereitet!"
    else:
        text = "Was hast du gesagt?" 
        print(">>>"+text)
    mainSpeaking(text)

#beleidigungen
def affront():
    text = "Keine Kraftausdrücke meine Lieben"
    mainSpeaking(text)

def mehrmals():
    text = "Einer nach dem anderen meine Lieben"
    print(">>>"+text)
    mainSpeaking(text)

def wunsch():
    text = "Ich kann dir einen "
    for drink in Cocktail.cocktails:
        text += drink.name[0]
        if Cocktail.cocktails.index(drink) is not len(Cocktail.cocktails)-1:
            text += ' oder '
    text += ' mixen.'
    print(">>>"+text)
    mainSpeaking(text)

#lange keine Interaktion mehr: Befehl
def talkToMe():
    text = "Ai karamba, ist denn hier niemand durstig? Wer hat noch nicht, wer will nochmal?"
    mainSpeaking(text)   

def automaticalyTurnOff(): 
    text = "Die Party war der Hammer! Zeit adios amigos zu sagen. Turn off in 3 2 1 Boooom!"
    mainSpeaking(text)

def turnoff():
    automaticalyTurnOff()
    sys.exit(0)

def mainListen():
    global cockInProgress
    sentence = dicti["speech"].lower().split()
    print(sentence)

    for word in sentence:
        #abbruch
        if word in abbruch:
            abbrechen()
            break

        #algo ausschalten
        if word in algooff:
            turnoff()

        #beleidigung, reagieren aber nicht abbrechen
        if word in insult or word[1] == '*':
             affront()

        #mehr als einer
        if word in mehr:
            next = sentence[sentence.index(word)+1]
            if next in Cocktail.cocktailNames:
                mehrmals()
                break

        #welche C gibt es
        if word in suggestion:
            wunsch()
            break

        #Cocktailname
        if word in Cocktail.cocktailNames and not cockInProgress:
            changecock()
            #befehl vor Cocktail
            if len(sentence) > 1:
                prev = sentence[0:sentence.index(word)-1]
                if sentence.index(word) == 1:
                    prev = sentence[sentence.index(word)-1]
                    if prev in befehl:
                        dicti['noCocktail']=False
                        dicti["lastCocktail"]= word
                        bekannt(word)
                else:
                    for w in prev:
                        if w in befehl:
                            dicti['noCocktail']=False
                            dicti["lastCocktail"]= word
                            bekannt(word)
                break
            #Nur Cocktailname
            else:
                dicti['noCocktail']=False
                dicti["lastCocktail"]= word
                bekannt(word)
                break

        #Cocktail gibts nicht
        if word in noCocktail:
            if len(sentence) > 1:
                #befehl vor Cocktail
                prev = sentence[0:sentence.index(word)-1]
                for w in prev:
                    if w in befehl:
                        dicti['noCocktail']=True
                        dicti["lastCocktail"]= word
                        unbekannt(word)
                break   
            #Nur Cocktailname
            else:
                dicti['noCocktail']=True
                dicti["lastCocktail"]= word
                unbekannt(word)
                break

        #selben Cocktail
        if word in vorherigen and not cockInProgress:
            changecock()
            #letzter Cocktail gabs nicht
            if dicti['noCocktail'] is True:
                unbekannt(dicti["lastCocktail"])
                break
            #gibt keinen vorherigen Cocktail
            elif dicti["lastCocktail"] == "":
                mainSpeaking("Du musst dir selbst etwas aussuchen")
                wunsch()
                break
            else:
                bekannt(dicti["lastCocktail"])
                break

        #überraschungscocktail
        if word in surprise and not cockInProgress:
            changecock()
            bekannt(Cocktail.cocktails[randint(0,2)].name[0])
            break

        #music an und ausschalten
        if word in musicoff:
            if len(sentence) > 1:
                prev = sentence[sentence.index(word)-1]
                if prev in musicname:
                    turnmusic()
                break

        if word in musicon:
            if len(sentence) > 1:
                prev = sentence[sentence.index(word)-1]
                if prev in musicname:
                    turnmusic() 
                break   

        #nach letztem wort immer noch nicht verstanden
        if sentence.index(word) == len(sentence)-1:
            unverstaendlich()
            break
    

def mainSpeaking(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)     
    engine.setProperty('volume',1.0)   
    voices = engine.getProperty('voices')  
    engine.setProperty('voice', voices[language].id)

    engine.say(text)
    engine.runAndWait()
    engine.stop()

def playSong(cocktail):
    if music:
        pygame.init()
        #pygame.mixer.music.load(cocktail.lied)
        pygame.mixer.music.load("./AlgoSpritz/" + cocktail.lied)
        pygame.mixer.music.play()
        print("Lied " , cocktail.lied , " spielt " , cocktail.pumpZeit() , "Sekunden")
        threading.Timer(cocktail.pumpZeit(), pygame.mixer.music.pause).start()
    else:
        print("du hast die musik ausgemacht")

def recognize():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Please say something")
        audio = r.listen(source, phrase_time_limit=5)
        print("Recognizing Now .... ")
        # recognize speech using google
        try:
            result = r.recognize_google(audio, language='de-DE')
            print("You have said \n" + result)
            dicti["speech"]=result
            mainListen()

        except Exception as e:
            print("Error :  " + str(e))
            #mainSpeaking("Was kann ich dir anbieten?")

def main():
    timeout = time.time() + 60*5  #*5 für 5 Minuten
    text= "Hey was geht? Ich bin AlgoSpritz, dein persönlicher Cocktailautomat! Lasset die Party starten!"
    mainSpeaking(text)
    while True:
        if time.time() > timeout:
            automaticalyTurnOff()
            break
        else:
            recognize()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            #pump.abbruch()
            pygame.mixer.music.pause()
            sys.exit(0)
        except SystemExit:
            os._exit(0)




