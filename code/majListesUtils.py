'''
    Prend en paramètres la partie (le plateau surtout)
    Met à jour le rôle de nos cellules et retourne une liste de 3 listes :
        la liste de nos rushers, de nos fournisseurs, et de nos attaquants
'''

def majRoles(partie) :
    noeuds = partie.plateau["noeuds"]
    rushers = []
    fournisseurs = []
    attaquants = []
    for cle in noeuds :
        if noeuds[cle].proprio == partie.me :
            role = ""
            #si le noeud est à nous
            #test si le noeud est un rusher
            #est-ce qu'il existe une cellule neutre à portée
            for ligne in noeuds[cle].aretesConnectees :
                if ligne.noeud1.proprio == -1 or ligne.noeud2.proprio == -1 :#-1 = neutre
                    role = 'rusher'
                    rushers.append(noeuds[cle])
                    break#pas la peine d'aller plus loin, on a trouvé un neutre à proximité, notre cellule est un rusher
                elif ligne.neud1.proprio != partie.me or ligne.noeud2.proprio != partie.me : #si on a un ennemi à proximité
                    role = "attaquant"
                    attaquants.append(noeuds[cle])
                    break#on arrete les frais, si on est pas un rusher, on a pas de neutre à proximité, donc dés qu'on a un ennemi, c'est qu'on est attaquant
                else : #on n'a pas de neutres ni d'attaquants à proximité, on est fournisseur
                    role = "fournisseur"
                    fournisseurs.append(noeuds[cle])

            noeuds[cle].role = role
    return {"rushers":rushers,"fournisseurs":fournisseurs,"attaquants":attaquants}
