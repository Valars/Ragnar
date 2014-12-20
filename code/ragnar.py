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

def register_pooo(uid):
    global partie
    partie = Partie("",uid)

def init_pooo(init_string):
    global partie
    uid = partie.uid
    partie = parseInit(init_string)
    partie.uid = uid


def play_pooo():
    global partie
    """Active le robot-joueur

    """
    #logging.info('Entering play_pooo fonction from {} module...'.format(inspect.currentframe().f_back.f_code.co_filename))
    #met à jour tous nos objets de plateau, noeuds, mouvements etc etc
    majPlateau(parseState(state()), partie.plateau)
    while True :

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
        a = input()
        if a == "fin" :
            break