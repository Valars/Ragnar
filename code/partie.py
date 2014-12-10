class Partie :
    def __init__(self, matchid="", uid="", speed=-1, me=-1, plateau=[]):
        self.matchid = matchid
        self.uid = uid
        self.speed = speed
        self.me = me
        self.plateau = plateau

    def printPartie(self) :
        print(self.uid+"@"+self.matchid)
        print("vitesse : "+str(self.speed)+" je suis le joueur "+str(me))
