import speech_recognition as sr

#alk = ['pina colada', 'gin tonic', 'sex on the beach']
alk =['hallo']
def findWords(result):
    print("YEAAAH")
    print(result[2])
    #for sorts in alk:
     #   if sorts in result:
      #      print(sorts)
    for r in result:
        print(r)
        print("\n")


def main():

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
            findWords(result)

        except Exception as e:
            print("Error :  " + str(e))


        # write audio
        with open("recorded.wav", "wb") as f:
            f.write(audio.get_wav_data())

if __name__ == "__main__":
    main()