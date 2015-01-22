# -*- coding: utf-8 -*-

from poooc import order, state, state_on_update, etime
from getObjects import *
from mouvement import *
from arete import *
#[0947e717-02a1-4d83-9470-a941b6e8ed07]MOV33FROM1TO4

''' Nom : mouv(laPartie, expediteur, cible, units)

    Role : Envoi d'un ordre de mouvement
    Description : Concatène les informations nécessaire en une chaine de caractères et appel la fonction order avec cette même chaine
        Crée un objet mouvement qui sera prit en compte pour la suite des décisions (ou pas xD)
    E : laPartie   : Partie : Informations de bases sur la partie en cours
        expediteur : Noeud  : Noeud envoyant les unités
        cible      : Noeud  : Noeud destinataire des unités
        units      : Int    : Pourcentage des unités de l'expediteur qui seront envoyés
'''

def mouv(partie, expediteur, cible, units):

    print("###################################")
    print("###################################")
    print("###################################")
    order("["+str(partie.uid)+"]MOV"+str(units)+"FROM"+str(expediteur.id)+"TO"+str(cible.id))
    arete = getArete(partie, expediteur.id, cible.id)
    arete.mouvements.append(Mouvement(cible, expediteur.off*units//100, etime(), expediteur.proprio))
    expediteur.off = expediteur.off - (expediteur.off*units//100) #on enleve ce qu'on a envoyé
