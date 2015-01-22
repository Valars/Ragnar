'''Nom : Mouvement

Attributs : destination : Noeud : Noeud de destination
            nbUnites    : Int   : Nombre d'unité offensive en cours de déplacement pour ce mouvement
            timeDepart  : Int   : Timestamp (etime) lors de l'envoi du mouvement
            joueur      : Int   : Joueur proprietaire des unités (cf. Partie.me)

'''
class Mouvement :
    def __init__(self, destination, nbUnites, timeDepart, joueur) :
        self.destination = destination
        self.nbUnites = nbUnites
        self.timeDepart = timeDepart
        self.joueur = joueur
