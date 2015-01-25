
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

    noeudsEnDanger = [ noeud[0] for noeud in noeudsEnDanger ]
    voisins = getVoisins(fournisseur)
    auFront, voisinsAuFront  = False, []
    
    if fournisseur.aretesConnectees == 1 : # Si le fournisseur n'a qu'un seul voisin, il lui envoit toutes ses unités
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
            
        # Si il n'y a pas de noeuds en danger
        if len(noeudsEnDanger) == 0 : 
			
            # Si on est en début de partie, et qu'il existe des voisins rushers et des attaquants sur le plateau
            if debutDePartie and len(voisinsRushers) > 0 and len(noeudsAttaquants) > 0 :
                
                mouv(partie, fournisseur, voisinsRushers[0], 25)
                noeudIntermediaire = fournisseur.distances[str(noeudsAttaquants[0].id)][0]
                noeudIntermediaire = getNoeud(partie, noeudIntermediaire)
                mouv(partie, fournisseur, noeudIntermediaire, 75)
            
            # Si on n'est pas en début de partie
            elif not debutDePartie and len(voisinsRushers) > 0 and len(noeudsAttaquants) > 0 :

                mouv(partie, fournisseur, voisinsRushers[0], 50)
                noeudIntermediaire = fournisseur.distances[str(noeudsAttaquants[0].id)][0]
                noeudIntermediaire = getNoeud(partie, noeudIntermediaire)
                mouv(partie, fournisseur, noeudIntermediaire, 50)
                
            else :
                if len(voisinsRushers) == 0 and len(noeudsAttaquants) > 0 : # Si il n'y a pas de voisins rushers

                    noeudIntermediaire = fournisseur.distances[str(noeudsAttaquants[0].id)][0]
                    noeudIntermediaire = getNoeud(partie, noeudIntermediaire)
                    mouv(partie, fournisseur, noeudIntermediaire, 100)
                elif len(voisinsRushers) > 0 and len(noeudsAttaquants) == 0 : # Si il n'y a pas d'attaquants

                    mouv(partie, fournisseur, voisinsRushers[0], 100)
                    
        # Sinon si il y'a des noeuds en danger 
        else :

            # Si mon voisin est un noeud en danger, je considère que je suis proche du front.
            for noeud in noeudsEnDanger :
                if noeud in voisins :
                    auFront = True
                    voisinsAuFront.append(noeud)
            
            # Si je suis au front, j'envoie l'ensemble de mes unités vers mon voisin le plus rentable
            if auFront :
                voisinsAuFront = triLePlusRentable(voisinsAuFront,fournisseur)
                mouv(partie, fournisseur, voisinsAuFront[0], 100)
            else :
                noeudsEnDanger = triLePlusRentable(noeudsEnDanger,fournisseur)

                #Si on est en début de partie et qu'un voisin du fournisseur est un rusher :
                if debutDePartie and len(voisinsRushers) > 0 :
					
                    mouv(partie, fournisseur, voisinsRushers[0], 50) # Envoie 50% de ses unités vers son voisin rusher
                    noeudIntermediaire = fournisseur.distances[str(noeudsEnDanger[0].id)][0]
                    noeudIntermediaire = getNoeud(partie, noeudIntermediaire)
                    mouv(partie, fournisseur, noeudIntermediaire, 50) # Envoie 50% de ses unités vers le noeud en danger le plus rentable
                
                else :
                    # Sinon, envoie 100% de ses unités vers le noeud en danger le plus rentable
                    noeudIntermediaire = fournisseur.distances[str(noeudsEnDanger[0].id)][0]
                    noeudIntermediaire = getNoeud(partie, noeudIntermediaire)
                    mouv(partie, fournisseur, noeudIntermediaire, 100)
