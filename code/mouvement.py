'''Nom : Mouvement

Attributs : destination : Noeud : Noeud de destination
            nbr         : Int   : Nombre d'unité offensive en cours de déplacement pour ce mouvement
            impact      : Int   : Temps restant avant arrivée à destination (en ms)
            proprio     : Int   : Joueur proprietaire des unités (cf. Partie.player)

'''
class Mouvement :
    def __init__(self, destination, nbUnites, duree, joueur) :
        self.destination = destination
        self.nbUnites = nbUnites
        self.duree = duree
        self.joueur = joueur
'''Nom : Mouvement

Attributs : destination : Noeud : Noeud de destination
            nbr         : Int   : Nombre d'unité offensive en cours de déplacement pour ce mouvement
            impact      : Int   : Temps restant avant arrivée à destination (en ms)
            proprio     : Int   : Joueur proprietaire des unités (cf. Partie.player)

'''
class Mouvement :
    def __init__(self, destination, nbUnites, duree, joueur) :
        self.destination = destination
        self.nbUnites = nbUnites
        self.duree = duree
        self.joueur = joueur
