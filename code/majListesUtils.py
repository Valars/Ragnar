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


'''
    Prend en paramètre la partie (surtout le plateau qui est important)
    Prend en second parametre notre liste de noeuds, qui nous appartiennent, ça fait gagner du temps, plutot que de retester tous les noeuds
    ce qu'on fait déjà dans la fonction juste au dessus :)

    retourne la liste des cellules en danger

    une cellule en danger est une cellule attaquante ou rusher, qui si l'adversaire le voulait, pourrait être capturée
    MAIS : la cellule pour l'instant ne va pas se faire capturer. Aucuns mouvements ne sont détectés dans sa direction qui pourrait la
    faire passer à l'ennemi :) il y a juste un statu quo, la cellule peut se faire bouffer, mais l'adversaire ne le fait pas.
'''
def calculDangers(partie, nosNoeuds) :
    cellulesEnDanger = []
    for noeud in nosNoeuds :
        #prendre tout ce qui se trouve à portée
