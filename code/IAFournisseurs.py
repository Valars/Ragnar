# -*- coding: utf-8 -*-

from fonctions_utiles import *
from mouv import *
from math import *

def IAFournisseurs(partie, dictRolesNoeuds, cellsDanger) :
    
    #cellsDanger : [[noeud, nbUnits pour sauver], [noeud, nbUnits pour sauver],...]
    #fournisseur : [Noeud, Noeud, Noeud,...]
    
    #On cree une liste des noeuds en danger sans le nombre d'unites necessaires pour le sortir du danger : necessaire pour utiliser 
    #la fonction triLePlusRentable qui est commune a ia rusher et ia fournisseur
    
    if(len(listeDesDangers) != 0):
        for fournisseur in dictRolesNoeuds["fournisseurs"]:
            
            dangersTries = triLePlusRentable(listeDesDangers, fournisseur)  #On trie les dangers selon leur rentabilite
        
            aideEnvoyee = False
            i  = 0
            
            while(aideEnvoyee == False and i < len(dangersTries)):                                
                besoin = dangersTries[i][2]    #On recupere le besoin en unites du noeud
                
                if(besoin <= fournisseur.off):                              #si le fournisseur a assez d'unites
                    a_envoyer = ceil((besoin/fournisseur.atk)*100)          #On calcul le pourcentage d'unites a envoyer
                    prochainNoeud = fournisseur.distances[str(dangersTries[i][0].id)][0] #on recupere le prochain noeud pour envoyer les renforts
                    
                    mouv(partie, fournisseur, prochainNoeud, a_envoyer)       #et on envoi (mouv actualise fournisseur.off et ajoute le mouvement correspond sur l'arete)
                    aideEnvoyee = True
                    
                    if(prochainNoeud == dangersTries[i]):       #Si le noeud en danger est voisin du fournisseur, alors il va automatiquement est sortie du danger dans peut de temps donc on le supprime de la liste
                        dangersTries.pop[i]
    
    nbNeutres = 0
    
    for noeud in partie.plateau["noeuds"] :         #On determine le nombre de neutres sur le plateau
        if (noeud.proprio == -1) : nbNeutres += 1
    
    if (nbNeutres >= len(partie.plateau["noeuds"])//2 - 1) : debutDePartie = True    #On regarde si on est en debut de partie (la moitie ou plus des noeuds sont des neutres)
    else : debutDePartie = False
        
    
    
    for fournisseur in dictRolesNoeuds["fournisseurs"]:  
        if (fournisseur.off > 0):
            
            if(debutDePartie): #Debut de partie donc on mise tout sur les rushers
                
                triRusherDist = triNoeudsDistances(dictRolesNoeuds["rushers"], fournisseur)
                
                prochainNoeud = fournisseur.distances[str(triRusherDist[1].id)][0][1]
                a_envoyer = 100
                
                mouv(partie, fournisseur, prochainNoeud, a_envoyer)
            else: #Pas debut de partie donc on soutient les attaquants
            
                triAttaquantDist = triNoeudsDistances(dictRolesNoeuds["attaquant"], fournisseur)
                
                prochainNoeud = fournisseur.distances[str(triAttaquantDist[1].id)][0][1]
                a_envoyer = 100
                
                mouv(partie, fournisseur, prochainNoeud, a_envoyer)
    
