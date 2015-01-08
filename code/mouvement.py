'''Nom : Mouvement

Attributs : destination : Noeud : Noeud de destination
            nbUnites    : Int   : Nombre d'unité offensive en cours de déplacement pour ce mouvement
            duree       : Int   : Temps restant avant arrivée à destination (en ms)
            joueur      : Int   : Joueur proprietaire des unités (cf. Partie.me)

'''
class Mouvement :
    def __init__(self, destination, nbUnites, duree, joueur) :
        self.destination = destination
        self.nbUnites = nbUnites
        self.duree = duree
        self.joueur = joueur
