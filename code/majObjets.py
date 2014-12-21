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
    for cleLigne in plateau["lignes"] :
        plateau["lignes"][cleLigne].mouvements = []

    for move in moves :
        #destination, nbUnites, duree, joueur
        if move["direction"] == '<' :
            iddestination = move["from"]
        else :
            iddestination = move["to"]

        destination = plateau["noeuds"][str(iddestination)]#on récupère l'objet noeud via l'id grace au dictionaire qui stocke les noeuds du plateau
        #récupérer l'arete qui part  de move["from"] et qui va a move["to"]
        #lui mettre à jour son arete.mouvements pour y append Mouvement(destination, move["nbUnits"], move["timestamp"], move["joueur"])

        #récupérer un objet arete via les id des noeuds extremités :
        cle = [str(move["from"])+";"+str(move["to"]), str(move["to"])+";"+str(move["from"])]

        try :
            arete = plateau["lignes"][cle[0]]
        except Exception :
            arete = plateau["lignes"][cle[1]]

        arete.mouvements.append(Mouvement(destination, move["nbUnits"], move["timestamp"], move["joueur"]))
