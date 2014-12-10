'''Nom : Partie

Attributs : matchid : Chaine de caractères : Identifiant de la partie
            userid  : Chaine de caractères : Identifiant du joueur pour tout le tournoi
            player  : Int                  : Identifiant du joueur dans la partie
            vitesse : Int                  : Donne la vitesse du jeu (Hypothétique)
            plateau : Liste                : Contient la liste des objets Noeud ainsi que la liste des objets Arete de
                                              tout le plateau
'''

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
