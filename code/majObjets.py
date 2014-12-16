from mouvement import *
#fonction mettant à jour le plateau en fonction du résultat de la fonction parseState()
def majPlateau(changements, plateau) :

    noeudsDyn = changements["noeuds"]
    moves = changements["moves"]

    #   mettre à jour les off et deff et proprio des cellules
    for noeudDyn in noeudsDyn :
        plateau["noeuds"][str(noeudDyn["id"])].off = noeudDyn["atk"]
        plateau["noeuds"][str(noeudDyn["id"])].defenses = noeudDyn["def"]
        plateau["noeuds"][str(noeudDyn["id"])].proprio = noeudDyn["owner"]

    #mettre a jour les aretes dans plateau["lignes"] pour ajouter les mouvements (objets à créer pour chaque move)
    objetsMouv = []
    fromTo = []
    for move in moves :
        #destination, nbUnites, duree, joueur
        if move["direction"] == '<' :
            iddestination = move["from"]
        else :
            iddestination = move["to"]

        for id in plateau["noeuds"] :
            if int(id) == iddestination :
                destination = plateau["noeuds"][id]

        #maintenant on veut récupérer un objet arete de plateau["ligne"] en le désignant par les id des noeuds
        #à faire donc, récupérer l'arete ayant pour extremités les noeuds d'id move["from"] et move["to"]

        objetsMouv.append(Mouvement(destination, move["nbUnits"], move["timestamp"], move["joueur"]))

    #puis pour chaque mouvement de objetsMouv, mettre les aretes à jour dans plateau["lignes"]
    #un mouvement va dans une arete si destination
