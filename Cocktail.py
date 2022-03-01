class Cocktail:
    def __init__(self,name,lied,**zutat):
        self.name = name
        self.inhalt = {'rum':0,'gin':0, 'limette':0, 'wasser':0, 'sirup':0}
        self.inhalt.update(zutat)
        self.lied = lied
    
    def pumpZeit(self):
        maxTime = max(self.inhalt.values()) + 10 # evtl Zeit drauf rechnen
        # maxTime = sum(self.inhalt.values())
        return maxTime

    def __repr__(self):
        return "Cocktail('{}','{}')".format(self.name,self.inhalt)

#Cocktails definieren
 
mojito = Cocktail(['mojito'],'music/Mojito.mp3',rum=16,limette=14,wasser=60,sirup=10)
caipi = Cocktail(['caipirinha','caipi'],'music/Caipirinha.mp3',rum=14,limette=16,wasser=20)
ginsour = Cocktail(['ginsour','gin sour','gin'],'music/GinSour.mp3',gin=20,limette=14,wasser=40,sirup=10)
cocktails = [mojito,caipi,ginsour]

cocktailNames = mojito.name + caipi.name + ginsour.name