# -*- coding: utf-8 -*-

from fonctions_utiles import *
from mouv import *
from math import *
import time


def IAFournisseurs(partie, fournisseur, noeudsEnDanger) :
    """ IA des noeuds Fournisseurs :
        Input:  partie : objet partie
                idFournisseur : int
                noeudsEnDanger : liste de [noeud, nbUnitésAenvoyer] """
    voisins = getVoisins(fournisseur)
    auFront, voisinsAuFront  = False, []
    
    #print("Je suis le fournisseur", fournisseur.id)
    #print("mes voisins : voisins")
    if fournisseur.aretesConnectees == 1 : # Si le fournisseur n'a qu'un seul voisin, il lui envoit toutes ses unités
        #print("J'envoie toutes mes unités vers",voisins[0].id)
        mouv(partie, fournisseur, voisins[0], 100)
        return
    else : 
        # Liste des noeuds neutres sur le plateau (id)
        neutresEnJeu = [noeud for noeud in partie.plateau["noeuds"] if getNoeud(partie, noeud).proprio == -1] 
        # Liste des voisins du fournisseur qui sont "rusher"
        voisinsRushers = [noeud for noeud in getVoisins(fournisseur) if noeud.role == "rusher"]
        # Liste des nos noeuds attaquants
        noeudsAttaquants = [ getNoeud(partie,noeud) for noeud in partie.plateau["noeuds"] if getNoeud(partie, noeud).role == "attaquant"]
        
        # Si la moitié du plateau est neutre, on considère que nous sommes en début de partie
        if len(neutresEnJeu) >= (len(partie.plateau["noeuds"])//2) :
            debutDePartie = True
        else :
            debutDePartie = False
        
        if len(noeudsEnDanger) == 0 : # Si il n'y a pas de noeuds en danger
            
            #Si on est en début de partie, on répartie nos unités entre les attaquants (75%) et les rushers (25%)
            if debutDePartie and len(voisinsRushers) > 0 and len(noeudsAttaquants) > 0 :# Si il y a des voisins rushers et des attaquants
                mouv(partie, fournisseur, voisinsRushers[0], 25)
                mouv(partie, fournisseur, noeudsAttaquants[0], 75)
            elif not debutDePartie and len(voisinsRushers) > 0 and len(noeudsAttaquants) > 0 :
                mouv(partie, fournisseur, voisinsRushers[0], 50)
                mouv(partie, fournisseur, noeudsAttaquants[0], 50)
            else :
                if len(voisinsRushers) == 0 and len(noeudsAttaquants) > 0 : # Si il n'y a pas de voisins rushers
                    mouv(partie, fournisseur, noeudsAttaquants[0], 100)
                elif len(voisinsRushers) > 0 and len(noeudsAttaquants) == 0 : # Si il n'y a pas d'attaquants
                    mouv(partie, fournisseur, voisinsRushers[0], 100)
                    
        # Sinon si il y'a des noeuds en danger 
        else :
            
            # Si mon voisin est un noeud en danger, je considère que je suis proche du front.
            for noeud in noeudsEnDanger :
                if noeud[0] in voisins :
                    auFront = True
                    voisinsAuFront.append(noeud)
            
            # Si je suis au front, j'envoie l'ensemble de mes unités vers mon voisin le plus rentable
            if auFront :
                voisinsAuFront = triLePlusRentable(voisinsAuFront,fournisseur)
                mouv(partie, fournisseur, voisinsAuFront[0][0], 100)

            else :
                noeudsEnDanger = triLePlusRentable(noeudsEnDanger,fournisseur)
            
                #Si on est en début de partie et qu'un voisin du fournisseur est un rusher :
                if debutDePartie and len(voisinsRushers) > 0 : 
                    mouv(partie, fournisseur, voisinsRushers[0], 50) # Envoie 50% de ses unités vers son voisin rusher
                    noeudIntermediaire = fournisseur.distances[str(noeudsEnDanger[0][0].id)]
                    mouv(partie, fournisseur, noeudIntermediaire, 50) # Envoie 50% de ses unités vers le noeud en danger le plus rentable
                else :
                    # Sinon, envoie 100% de ses unités vers le noeud en danger le plus rentable
                    print(noeudsEnDanger)
                    print(noeudsEnDanger[0])
                    mouv(partie, fournisseur, noeudsEnDanger[0][0], 100)
