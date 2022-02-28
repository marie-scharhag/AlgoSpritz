import speech_recognition as sr
import time
#import pump
import pyttsx3
import pygame

#to do:
#Ansprechen
#Musik auschalten
#abbruch
#unverstaendlich


#languageID bei Sprachausgabe 0 bei Windows und 4 bei Mac
language = 4

class Cocktail:
    def __init__(self,name,lied,**zutat):
        self.name = name
        self.inhalt = {'rum':0,'gin':0, 'limette':0, 'wasser':0, 'sirup':0}
        self.inhalt.update(zutat)
        self.lied = lied
    
    def pumpZeit(self):
        self.maxTime = max(self.inhalt.values()) + 10 # evtl Zeit drauf rechnen
        return self.maxTime

    def __repr__(self):
        return "Cocktail('{}','{}')".format(self.name,self.inhalt)

#Cocktails definieren
mojito = Cocktail(['mojito'],'music/Mojito.mp3',rum=10,limette=5,wasser=20,sirup=5)
caipi = Cocktail(['caipi','caipirinha'],'music/Caipirinha.mp3',rum=10,limette=5,wasser=20)
ginsour = Cocktail(['ginsour','gin sour'],'music/GinSour.mp3',gin=10,limette=5,wasser=20,sirup=5)
cocktails = [mojito,caipi,ginsour]

cocktailNames = mojito.name + caipi.name + ginsour.name

# alk = ['caipirinha', 'mojito', 'gin sour']
noCocktail =['Cuba Libre','Gin Tonic','Moscow Mule', 'Negroni', 'Pina Colada', 'Tequila Sunrise','Cuba Libre','Zombie']
mehr = ['zwei','2','drei','3', 'mal','vier','4','und','2 x']
abbruch = ['abbruch','stopp', 'halt','abbrechen','nein']
vorherigen = ['auch', 'gleichen', 'letzten', 'vorherigen','selben']
befehl =['mix','mach','mache','hätte','nehme','nehm','will','möchte','gib']

dicti = {"speech":"","lastCocktail":"", "noCocktail": False}

def bekannt(cocktail):
    for c in cocktails:
        if cocktail in c.name:
            cock = c
    text = "Okay, ein "+cocktail+" wird jetzt gemixt!" 
    print(text)
    mainSpeaking(text)
    #pump.mixIT(cock)
    playSong(cock)

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
    for drink in cocktails:
        text += drink.name[0]
        if cocktails.index(drink) is not len(cocktails)-1:
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
            
            mainListen()

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
            if next in cocktailNames:
                mehrmals()
                break
        
        #Cocktailname
        if word in cocktailNames:
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
        if sentence.index(word) is len(sentence):
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
    time.sleep(cocktail.pumpZeit())
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




