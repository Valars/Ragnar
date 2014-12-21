# -*- coding: utf-8 -*-


## chargement de l'interface de communication avec le serveur
from poooc import order, state, state_on_update, etime

# mieux que des print partout
import logging
# pour faire de l'introspection
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
    print(uid)
    partie = Partie("",uid)

def init_pooo(init_string):
    global partie
    print(init_string)
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

#def state() :
#    return "STATEa16a58c2-81f0-4982-990b-ae4fdbcbd4ecIS2;7CELLS:0[0]5'0,1[-1]6'0,2[-1]6'0,3[-1]12'0,4[-1]6'0,5[-1]6'0,6[1]5'0;0MOVES"

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
        #ne marche qu'avec un input() ici !!!

        majPlateau(parseState(state_on_update()), partie.plateau)

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
        #partie.detailPlateau()#affichage du détail du plateau pour vérifier que tout est bien linké !
#register_pooo("amoii-45-qdfd")
#init_pooo("INITa16a58c2-81f0-4982-990b-ae4fdbcbd4ecTO2[0];2;7CELLS:0(0,0)'100'30'8'I,1(0,5)'100'30'8'I,2(5,0)'100'30'8'I,3(5,5)'200'30'8'II,4(5,10)'100'30'8'I,5(10,5)'100'30'8'I,6(10,10)'100'30'8'I;6LINES:0@4800OF2,0@4800OF1,2@4700OF3,3@4700OF4,4@4800OF6,5@4800OF6")
#play_pooo()
