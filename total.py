import speech_recognition as sr
import time
import pump
import pyttsx3


alk = ['caipirinha', 'mojito', 'gin sour']
notAlk =['wodka']
mehr = ['zwei','2','drei','3', 'mal','vier','4','und','2 x']
abbruch = ['abbruch','stopp', 'halt']
vorherigen = ['auch', 'gleichen', 'letzten', 'vorherigen']


dicti = {"speech":"","lastCocktail":"", "noAlk": False}

def bekannt(lastCocktail):
    test = 0
    for more in mehr:
        if more in dicti["speech"].lower():
            mehrmals()
            test = 1
        else:
            if test == 1:
                break  
            else: 
                text = "Okay, ein "+lastCocktail+" wird jetzt gemixt!" 
                print(text)
                mainSpeaking(text)
                pump.mixIT(lastCocktail)
                break

def unbekannt(lastCocktail):
    text = "t Tut mir leid, ich habe leider keinen "+lastCocktail+" in meinem Angebot. Möchtest du Vorschläge für andere Cocktails hören?"
    print(">>>"+text) 
    mainSpeaking(text)

def abbrechen():
    text = "Der Vorgang wird abgebrochen."
    print(">>>"+text)
    mainSpeaking(text)

def unverstaendlich():
    text = "Ich habe dich nicht verstanden, sage es bitte noch einmal." 
    print(">>>"+text)
    mainSpeaking(text)

def mehrmals():
    text = "Bitte bestelle einzeln."
    print(">>>"+text)
    mainSpeaking(text)

def wunsch():
    text = "Meine Top3 Cocktails sind...."
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
            unverstaendlich()
        

def mainListen():

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
    engine.setProperty('rate', 125)     
    engine.setProperty('volume',1.0)    
    voices = engine.getProperty('voices')       
    engine.setProperty('voice', voices[0].id)

    engine.say(text)
    engine.runAndWait()
    engine.stop()



def main():
    timeout = time.time() + 60  #*5 für 5 Minuten

    while True:
        if time.time() > timeout:
            break
        else:
            recognize()

if __name__ == "__main__":
    main()




