import speech_recognition as sr
import time
#import pump
import pyttsx3
import pygame

#to do:
#Ansprechen
#Musik auschalten
#Dauermusik auf Pumpe anpassen
#abbruch
#unverstaendlich



#languageID bei Sprachausgabe 0 bei Windows und 4 bei Mac
language = 4

alk = ['caipirinha', 'mojito', 'gin sour']
notAlk =['wodka']
mehr = ['zwei','2','drei','3', 'mal','vier','4','und','2 x']
abbruch = ['abbruch','stopp', 'halt','abbrechen','nein']
vorherigen = ['auch', 'gleichen', 'letzten', 'vorherigen','selben']
befehl =['mix','mach','mache','hätte','nehme','nehm','will','möchte','gib']

dicti = {"speech":"","lastCocktail":"", "noAlk": False}

def bekannt(cocktail):
    # test = 0
    # for more in mehr:
    #     if more in dicti["speech"].lower():
    #         mehrmals()
    #         test = 1
    #     else:
    #         if test == 1:
    #             break  
    #         else: 
    text = "Okay, ein "+cocktail+" wird jetzt gemixt!" 
    print(text)
    mainSpeaking(text)
    #pump.mixIT(cocktail)
    playSong(cocktail)
    # break

def unbekannt(cocktail):
    text = "Sorry leider fehlen mir die Zutaten für einen "+cocktail
    print(">>>"+text) 
    mainSpeaking(text)
    wunsch()

def abbrechen():
    text = "Ok ok ich hör ja schon auf"
    print(">>>"+text)
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
    for drink in alk:
        text += drink
        if alk.index(drink) is not len(alk)-1:
            text += ' oder '
    text += ' mixen.'
    print(">>>"+text)
    mainSpeaking(text)

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
            
            mainListen2()

        except Exception as e:
            print("Error :  " + str(e))
            mainSpeaking("Was kann ich dir anbieten?")
        

def mainListen():

    sentence = dicti["speech"].lower().split()

    for word in sentence:
        #abbruch
        if word in abbruch:
            abbrechen()
            break

        #mehr als einer
        if word in mehr:
            next = sentence[sentence.index(word)+1]
            if next in alk:
                mehrmals()
                break
        
        #Cocktailname
        if word in alk:
            #befehl vor Cocktail
            if len(sentence) > 1:
                prev = sentence[0:sentence.index(word)-1]
                for w in prev:
                    if w in befehl:
                        dicti['noAlk']=False
                        dicti["lastCocktail"]= word
                        bekannt(word)
                        break
            #Nur Cocktailname
            else:
                dicti['noAlk']=False
                dicti["lastCocktail"]= word
                bekannt(word)
                break

        #Cocktail gibts nicht
        if word in notAlk:
            if len(sentence) > 1:
                #befehl vor Cocktail
                prev = sentence[0:sentence.index(word)-1]
                for w in prev:
                    if w in befehl:
                        dicti['noAlk']=True
                        dicti["lastCocktail"]= word
                        unbekannt(word)
                        break
            #Nur Cocktailname
            else:
                dicti['noAlk']=True
                dicti["lastCocktail"]= word
                unbekannt(word)
                break

        #selben Cocktail
        if word in vorherigen:
            #letzter Cocktail gabs nicht
            if dicti['noAlk'] is True:
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
        if sentence.index(word) is len(sentence):
            unverstaendlich()
            break
        
def mainListen2():

    for sorts in alk:
        if sorts in dicti["speech"].lower():
            dicti["lastCocktail"]= sorts
            bekannt(dicti["lastCocktail"]) 
          
    for vor in vorherigen:
        if vor in dicti["speech"].lower():
            bekannt(dicti["lastCocktail"])

    for abb in abbruch:
        if abb in dicti["speech"].lower():
            abbrechen() 
            
    unverst = alk + mehr +abbruch +vorherigen+notAlk
    unverst.append('ja') 
    #hasIt = any(dicti["speech"].lower() in a for a in unverst)
    #print(hasIt) 
    #if hasIt == False:
    #   unverstaendlich()
    #print(hasIt)

    b = 0
    for a in unverst:
        if a in dicti['speech'].lower():
            b = 1
    if b==0:
        unverstaendlich()
                


    for noo in notAlk:
        if noo in dicti['speech'].lower():
            dicti["lastCocktail"]=noo
            unbekannt(dicti["lastCocktail"])
            dicti['noAlk']=True


    if 'ja' in dicti["speech"].lower():
        if dicti['noAlk']==True:        
            print("juhuu")
            wunsch()
            dicti['noAlk']=False
 
    print(dicti)

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
    if cocktail =="caipirinha":
        path="music/Caipirinha.mp3" 
        dauer= 25    
    elif cocktail =="mojito":
        path="music/Mojito.mp3"
        dauer =25
    elif cocktail =="gin sour":
        path = "music/GinSour.mp3"
        dauer = 25

    pygame.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    time.sleep(dauer)
    pygame.mixer.music.pause()

def main():
    timeout = time.time() + 60*5  #*5 für 5 Minuten
    text= "Heeeeey was geht? Ich bin Algospritz, dein persönlicher Cocktailautomat! Was magst du trinken?"
    mainSpeaking(text)
    while True:
        if time.time() > timeout:
            break
        else:
            recognize()

if __name__ == "__main__":
    main()




