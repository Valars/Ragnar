#fonction mettant à jour le plateau en fonction du résultat de la fonction parseState()
def majPlateau(changements) :
    noeuds = changements["noeuds"]
    moves = changements["moves"]
    print("NOEUDS : ")
    for noeud in noeuds :
        print(noeud)
