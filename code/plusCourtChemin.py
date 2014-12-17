#retourne la liste des noeuds qu'il faut parcourir pour aller du noeud from au noeud to
# from : noeud
#to : noeud
#retourne : liste de noeuds (plus court chemin entre from et to)
def plusCourtChemin(de, vers) :
    parcouru = []
    possibles = [de]
    courant = de
    fin = False

    while courant != vers and fin != True :

        for aretevoisine in courant.aretesConnectees :
            if aretevoisine.noeud1 == courant :
                levoisin = aretevoisine.noeud2
            else :
                levoisin = aretevoisine.noeud1
            if levoisin == vers :
                parcouru.append(courant)
                parcouru.append(levoisin)
                fin = True
            else :
                possibles.append(levoisin)
        if fin == False :
            parcouru.append(courant)
            possibles.pop(0)
        courant = possibles[0]
    return parcouru
