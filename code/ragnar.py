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




def register_pooo(uid):
    global partie
    partie = Partie("",uid)

def init_pooo(init_string):
    global partie
    uid = partie.uid
    partie = parseInit(init_string)
    partie.uid = uid



def play_pooo():
    """Active le robot-joueur

    """
    logging.info('Entering play_pooo fonction from {} module...'.format(inspect.currentframe().f_back.f_code.co_filename))

    ### Début stratégie joueur ###
    # séquence type :
    # (1) récupère l'état initial
    # init_state = state()
    # (2) TODO: traitement de init_state
    # (3) while True :
    # (4)     state = state_on_update()
    # (5)     TODO: traitement de state et transmission d'ordres order(msg)


register_pooo("0947e717-02a1-4d83-9470-a941b6e8ed07")
init_pooo("INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;2CELLS:1[2]23'9'2'30'8'1,2[1]41'55'1'30'8'2;2LINES:1@3433OF2,1@6502OF3")
play_pooo()
