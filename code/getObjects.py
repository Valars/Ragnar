'''Nom : getArete()

E : partie   : Partie : Instance de la partie en cours
    idNoeud1 : Noeud  : Identifiant de l'un des noeud extremité de l'arete souhaité
    idNoeud2 : Noeud  : Identifiant du second noeud extremité de l'arete souhaité

S :          : Arete  : réference vers l'arete souhaité
'''

def getArete(partie, idNoeud1, idNoeud2):
    return partie.plateau["lignes"][str(idNoeud1)+";"+str(idNoeud2)]

'''Nom : getNoeud()

E : partie : Partie : Instance de la partie en cours
    id     : Int    : Id du Noeud souhaité

S :        : Arete  : réference vers le noeud souhaité
'''

def getNoeud(partie, id) :
    return partie.plateau["noeuds"][str(id)]

''' Nom : getVoisins()
E : noeud : objet Noeud dont on veut obtenir les noeuds voisins

S : Liste : liste d'objets Noeud, qui sont les voisins de l'entrée noeud
'''
def getVoisins(noeud) :
    voisins = []
    for ligne in noeud.aretesConnectees :
        if ligne.noeud1 == noeud :
            voisins.append(ligne.noeud2)
        else :
            voisins.append(ligne.noeud1)
    return voisins

def getDistance(noeud1, noeud2) :
    return noeud1.distances[str(noeud2.id)]
