from getObjects import *
''' Nom : majRoles(partie):
        
    E : laPartie   : Partie : Informations de bases sur la partie en cours

    S :            : Liste  : Liste des trois listes de Noeud correspondantent aux "rushers", "fournisseurs" et "attaquants"
'''

def majRoles(partie) :
    noeuds = partie.plateau["noeuds"]
    rushers = []
    fournisseurs = []
    attaquants = []
    
    for noeud in noeuds :
        neutreTrouve = False
        ennemiTrouve = False
        if noeuds[noeud].proprio == partie.me :
            voisins = getVoisins(noeuds[noeud])
            for voisin in voisins :
                if voisin.proprio == -1 :
                    neutreTrouve = True
                else :
                    if voisin.proprio != noeuds[noeud].proprio :
                        ennemiTrouve = True
            if neutreTrouve :
                noeuds[noeud].role = "rusher"
                rushers.append(noeuds[noeud])
            else :
                if ennemiTrouve :
                    noeuds[noeud].role = "attaquant"
                    attaquants.append(noeuds[noeud])
                else :
                    noeuds[noeud].role = "fournisseur"
                    fournisseurs.append(noeuds[noeud])
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

''' Nom : calculDangersCapturees(partie, nosNoeuds):
        
    E : laPartie   : Partie : Informations de bases sur la partie en cours
        nosNoeuds  : Liste  : Liste de nos noeuds (rushers+fournisseurs+attaquants)

    S :            : Liste  : Liste des deux listes de Noeud correspondantent aux cellules en danger ("dangers") et celles qui vont etre capturees ("capturees")
'''
def calculDangersCapturees(partie, nosNoeuds) :
    cellulesEnDanger = []
    cellulesCapturees = []
    for noeud in nosNoeuds :
        #prendre tout ce qui arrive sur les arêtes
        forces = 0
        for ligne in noeud.aretesConnectees :
            mouvements = ligne.mouvements
            for mouvement in mouvements :
                if mouvement.destination == noeud and mouvement.joueur != partie.me :
                    forces += mouvement.nbUnites
        if forces >= (noeud.off + noeud.defenses) : #si les forces qui nous arrivent dans le museau son supérieures à ce qu'on peut encaisser
            #alors on va se faire capturer
            cellulesCapturees.append([noeud, forces-noeud.off-noeud.defenses])#on enregistre le noeud dans les cellules qui vont se faire capturer + la différence de forces
        

        else :#dessous ce else, la cellule ne va pas se faire capturer, il faut cependant vérifier si elle est en danger
            if noeud.role == "attaquant" or noeud.role == "rusher" : #seuls les attaquants et les rushers peuvent se faire capturer
                total = 0#total des forces ennemies à proximité
                for ligne in noeud.aretesConnectees :
                    if ligne.noeud1 == noeud :
                        voisin = ligne.noeud2
                    else :
                        voisin = ligne.noeud1
                    #voisin = on a récupéré le voisin de notre noeud courant
                    if voisin.proprio not in [-1, partie.me] : #si le proprio du voisin n'est ni "neutre" ni "nous" : alors ennemi !
                        total += voisin.off #on incrémente le total des forces ennemies
                if total >= (noeud.off + noeud.defenses) : #si le total des forces ennemies à proximité est supérieur à ce qu'on peut encaisser : danger
                    cellulesEnDanger.append([noeud, total-noeud.off-noeud.defenses])


    return {"dangers":cellulesEnDanger,"capturees":cellulesCapturees}
