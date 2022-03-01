import speech_recognition as sr
import time
import pump
import Cocktail
import pyttsx3
import pygame
import threading
import sys
import os

#to do:
#Musik auschalten
#abbruch


#languageID bei Sprachausgabe 0 bei Windows und 4 bei Mac
language = 4

noCocktail =['Cuba Libre','Gin Tonic','Moscow Mule', 'Negroni', 'Pina Colada', 'Tequila Sunrise','Cuba Libre','Zombie']
mehr = ['zwei','2','drei','3', 'mal','vier','4','und','2 x']
abbruch = ['abbruch','stopp', 'halt','abbrechen','nein']
vorherigen = ['auch', 'gleichen', 'letzten', 'vorherigen','selben']
befehl =['mix','mach','mache','hätte','nehme','nehm','will','möchte','gib']

dicti = {"speech":"","lastCocktail":"", "noCocktail": False}

def bekannt(cocktail):
    for c in Cocktail.cocktails:
        if cocktail in c.name:
            cock = c
    text = "Okay, ein "+cocktail+" wird jetzt gemixt!" 
    print(text)
    mainSpeaking(text)
    playSong(cock)
    pump.mixIT(cock)

def unbekannt(cocktail):
    text = "Sorry leider fehlen mir die Zutaten für einen "+cocktail
    print(">>>"+text) 
    mainSpeaking(text)
    wunsch()

def abbrechen():
    text = "Ok ok ich hör ja schon auf"
    #musik und pumpen abbrechen
    print(">>>"+text)
    pygame.mixer.music.pause()
    pump.abbruch()
    mainSpeaking(text)

def unverstaendlich():
    text = "Was hast du gesagt?" 
    print(">>>"+text)
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
        

def mainListen():

    sentence = dicti["speech"].lower().split()
    print(sentence)

    for word in sentence:
        #abbruch
        if word in abbruch:
            abbrechen()
            break

        #mehr als einer
        if word in mehr:
            next = sentence[sentence.index(word)+1]
            if next in Cocktail.cocktailNames:
                mehrmals()
                break
        
        #Cocktailname
        if word in Cocktail.cocktailNames:
            #befehl vor Cocktail
            if len(sentence) > 1:
                prev = sentence[0:sentence.index(word)-1]
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
        if word in vorherigen:
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
    pygame.init()
    pygame.mixer.music.load(cocktail.lied)
    pygame.mixer.music.play()
    print("Lied " , cocktail.lied , " spielt " , cocktail.pumpZeit() , "Sekunden")
    threading.Timer(cocktail.pumpZeit(), pygame.mixer.music.pause).start()

def recognize():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        print("Please say something")
        audio = r.listen(source)
        print("Recognizing Now .... ")
        # recognize speech using google
        try:
            result = r.recognize_google(audio, language='de-DE')
            print("You have said \n" + result)
            print("Audio Recorded Successfully \n ")
            dicti["speech"]=result
            
            # if "abbruch" in result.lower():
            #     abbrechen()
            # else:
            mainListen()

        except Exception as e:
            print("Error :  " + str(e))
            mainSpeaking("Was kann ich dir anbieten?")

def main():
    timeout = time.time() + 60*5  #*5 für 5 Minuten
    text= "Hey was geht? Ich bin AlgoSpritz, dein persönlicher Cocktailautomat! Beginne jeden Befehl mit AlgoSpritz. Lasset die Party starten!"
    mainSpeaking(text)
    while True:
        if time.time() > timeout:
            break
        else:
            recognize()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            pump.abbruch()
            pygame.mixer.music.pause()
            sys.exit(0)
        except SystemExit:
            os._exit(0)




