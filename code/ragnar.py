# -*- coding: utf-8 -*-


## chargement de l'interface de communication avec le serveur
from poooc import order, state, state_on_update, etime

# mieux que des print partout
import logging
# pour faire de l'introspection
import re
import inspect
from arete import *
from noeud import *
from parsers import *
from partie import *
from majObjets import *
from getObjects import *
from mouv import *
from plusCourtChemin import *
from tkinter import *

def register_pooo(uid):
    global partie
    partie = Partie("",uid)

def init_pooo(init_string):
    global partie
    uid = partie.uid
    partie = parseInit(init_string)
    partie.uid = uid

def affichageGraphique(canva) :
    global partie
    coords = [[0,100],[0,400],[400,100],[400,400],[200,0],[200,500],[100,450]]
    for cle in partie.plateau["noeuds"] :
        partie.plateau["noeuds"][cle].x = coords[partie.plateau["noeuds"][cle].id][0]
        partie.plateau["noeuds"][cle].y = coords[partie.plateau["noeuds"][cle].id][1]
        partie.plateau["noeuds"][cle].radius = 50
        partie.plateau["noeuds"][cle].afficher(canva)

    for cle in partie.plateau["lignes"] :
        partie.plateau["lignes"][cle].afficher(canva)

def play_pooo():
    global partie
    master = Tk()
    w = Canvas(master, width=800, height=800)

    """Active le robot-joueur

    """
    #logging.info('Entering play_pooo fonction from {} module...'.format(inspect.currentframe().f_back.f_code.co_filename))
    #met à jour tous nos objets de plateau, noeuds, mouvements etc etc
    majPlateau(parseState(state()), partie.plateau)

    while True :
        w.delete(ALL)
        affichageGraphique(w)
        w.update()

        retourServeur = state_on_update()
        states = retourServeur.split("STATE")
        unSeulState = "STATE"+states[1]

        majPlateau(parseState(unSeulState), partie.plateau)

        for cle in partie.plateau["noeuds"] :
            if partie.plateau["noeuds"][cle].proprio == partie.me :
                noeud = partie.plateau["noeuds"][cle]
                break
        mouv(partie, noeud, noeud.aretesConnectees[0].noeud2, 100)

        #---------------------#
        #-------Code IA-------#
        #---------------------#
    '''Données utilisables :
            partie
                partie.plateau
                    partie.plateau["noeuds"]
                    partie.plateau["lignes"]
                        qui sont deux dictionnaires, pour les noeuds, la clé de chaque noeud est son id (en string)
                        pour les lignes, la clé de chaque arete est "idnoeud1;idnoeud2"
                        par exemple pour le noeud d'id 2 : partie.plateau["noeuds"]["2"]
                        par exemple pour l'arete entre le noeud 1 et le noeud 3 : partie.plateau["lignes"]["1;3"]
                                                                                    ou partie.plateau["lignes"]["3;1"]
        Methodes utilisables :
            getArete(partie, id1, id2) - retourne l'ojet arete correspondant
            getNoeud(partie, id) - retourne l'objet noeud correspondant
            mouv(partie, expediteur, cible, units) - expediteur : objet noeud qui envoi, cible : objet noeud a qui on envoit, units : pourcentage des unités à envoyer'''

        #---------------------#
        #-----Fin code IA-----#
        #---------------------#
