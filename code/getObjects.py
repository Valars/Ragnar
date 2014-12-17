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
    
S :          : Arete  : réference vers le noeud souhaité
'''

def getNoeud(partie, id) :
    return partie.plateau["noeuds"][str(id)]