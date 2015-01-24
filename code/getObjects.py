'''Nom : getArete(partie, idnoeud1, idnoeud2)

    E : partie   : Partie : Instance de la partie en cours
        idNoeud1 : Int   : Identifiant de l'un des noeud extremité de l'arete souhaité
        idNoeud2 : Int   : Identifiant du second noeud extremité de l'arete souhaité
    
    S :          : Arete  : réference vers l'arete souhaité
'''

def getArete(partie, idNoeud1, idNoeud2):
    return partie.plateau["lignes"][str(idNoeud1)+";"+str(idNoeud2)]

'''Nom : getNoeud(partie, idnoeud)

    E : partie  : Partie : Instance de la partie en cours
        idnoeud : Int    : Id du Noeud souhaité
    
    S :         : Arete  : réference vers le noeud souhaité
'''

def getNoeud(partie, idnoeud) :
    return partie.plateau["noeuds"][str(idnoeud)]

''' Nom : getVoisins(noeud)

    E : Noeud : objet Noeud dont on veut obtenir les noeuds voisins
    
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

''' Nom : getDistance(noeud1, noeud2)

    E : noeud1 : Noeud : la premiere extremité du chemin dont on veut la distance
        noeud2 : Noeud : La seconde extremité du chemin dont on veut la distance
    
    S :          Int   : La distance du chemin
'''
def getDistance(noeud1, noeud2) :
    return noeud1.distances[str(noeud2.id)][1]
