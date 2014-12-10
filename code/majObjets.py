from partie import *
#fonction mettant à jour le plateau en fonction du résultat de la fonction parseState()
def majPlateau(changements, plateau) :

    noeuds = changements["noeuds"]
    moves = changements["moves"]
    print("moves : ")
    for move in moves :
        print(move)

    print(plateau)
