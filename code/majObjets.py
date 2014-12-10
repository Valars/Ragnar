from partie import *
#fonction mettant à jour le plateau en fonction du résultat de la fonction parseState()
def majPlateau(changements, plateau) :

    noeudsDyn = changements["noeuds"]
    moves = changements["moves"]

    #   mettre à jour les off et deff et proprio des cellules
    for noeudDyn in noeudsDyn :
        for noeud in plateau["noeuds"] :
            if noeud.id == noeudDyn["id"] :
                noeud.off = noeudDyn["atk"]
                noeud.defenses = noeudDyn["def"]
                noeud.proprio = noeudDyn["owner"]

    #mettre a jour les aretes dans plateau["lignes"] pour ajouter les mouvements (objets à créer pour chaque move)
    
