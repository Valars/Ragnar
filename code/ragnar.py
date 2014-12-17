# -*- coding: utf-8 -*-


## chargement de l'interface de communication avec le serveur
#from poooc import order, state, state_on_update, etime

# mieux que des print partout
import logging
# pour faire de l'introspection
import inspect
from arete import *
from noeud import *
from parsers import *
from partie import *
from majObjets import *
from getObjets import *

def state() :
    return "STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"


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

    while True :
        #met à jour tous nos objets de plateau, noeuds, mouvements etc etc   
        majPlateau(parseState(state()), partie.plateau)
        
        a=input()        
        if a == 'fin' :
            break
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
                                                                                    ou partie.plateau["lignes"]["3;1"]'''
        
        #---------------------#
        #-----Fin code IA-----#
        #---------------------#
    #partie.detailPlateau()#affichage du détail du plateau pour vérifier que tout est bien linké !

    ### Début stratégie joueur ###
    # séquence type :
    # (1) récupère l'état initial
    # init_state = state()
    # (2) TODO: traitement de init_state
    # (3) while True :
    # (4)     state = state_on_update()
    # (5)     TODO: traitement de state et transmission d'ordres order(msg)


register_pooo("0947e717-02a1-4d83-9470-a941b6e8ed07")
init_pooo("INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3")
play_pooo()
