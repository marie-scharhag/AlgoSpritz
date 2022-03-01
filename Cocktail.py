class Cocktail:
    def __init__(self,name,lied,**zutat):
        self.name = name
        self.inhalt = {'rum':0,'gin':0, 'limette':0, 'wasser':0, 'sirup':0}
        self.inhalt.update(zutat)
        self.lied = lied
    
    def pumpZeit(self):
        # maxTime = max(self.inhalt.values()) + 10 # evtl Zeit drauf rechnen
        maxTime = sum(self.inhalt.values())
        return maxTime

    def __repr__(self):
        return "Cocktail('{}','{}')".format(self.name,self.inhalt)

#Cocktails definieren
# rum=7,rum=7,
mojito = Cocktail(['mojito'],'music/Mojito.mp3',limette=7,wasser=30,sirup=5)
caipi = Cocktail(['caipirinha','caipi'],'music/Caipirinha.mp3',limette=5,wasser=5)
ginsour = Cocktail(['ginsour','gin sour','gin'],'music/GinSour.mp3',gin=10,limette=7,wasser=30,sirup=5)
cocktails = [mojito,caipi,ginsour]

cocktailNames = mojito.name + caipi.name + ginsour.name