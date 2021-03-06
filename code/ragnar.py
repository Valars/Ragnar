# -*- coding: utf-8 -*-


## chargement de l'interface de communication avec le serveur
from poooc import order, state, state_on_update, etime

import logging
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
from majListesUtils import *
from IAAttaquants import *
from IAFournisseurs import *
from IARushers import *
import time

def register_pooo(uid):
    global partie
    partie = Partie("",uid)

def init_pooo(init_string):
    global partie
    uid = partie.uid
    partie = parseInit(init_string)
    partie.uid = uid
    calc_distances(partie)

    for cle in partie.plateau["noeuds"] :
        partie.plateau["noeuds"][cle].x = partie.plateau["noeuds"][cle].x//20
        partie.plateau["noeuds"][cle].y = partie.plateau["noeuds"][cle].y//20
        partie.plateau["noeuds"][cle].radius = partie.plateau["noeuds"][cle].radius//3.5

def affichageGraphique(canva) :
    global partie
    coords = [[0,100],[0,400],[400,100],[400,400],[200,0],[200,500],[100,450]]
    for cle in partie.plateau["noeuds"] :
        partie.plateau["noeuds"][cle].afficher(canva)
    
    aretesAffichees = []
    offsety = 20
    for cle in partie.plateau["lignes"] :
        if cle not in aretesAffichees and cle[::-1] not in aretesAffichees :
            aretesAffichees.append(cle)
            partie.plateau["lignes"][cle].afficher(canva)
            for mouvement in partie.plateau["lignes"][cle].mouvements :
                canva.create_text(120,offsety,text="mouvement vers noeud"+str(mouvement.destination.id)+" de "+str(mouvement.nbUnites)+" de j"+str(mouvement.joueur),font=('Helvetica', 10),fill="red")
                offsety += 11

def play_pooo():
    global partie

    master = Tk()
    w = Canvas(master, width=1400, height=800)

    """Active le robot-joueur

    """
    #logging.info('Entering play_pooo fonction from {} module...'.format(inspect.currentframe().f_back.f_code.co_filename))
    #met à jour tous nos objets de plateau, noeuds, mouvements etc etc
    majPlateau(parseState(state()), partie.plateau)

    while True :

        #obligé de faire ce petit trick, le serveur envoi parfois deux states collés ...
        retourServeur = state_on_update()

        endofgame = retourServeur.split("ENDOFGAME")
        gameover = retourServeur.split("GAMEOVER")
        endofcontest = retourServeur.split("ENDOFCONTEST")
        if endofgame[0] == '' or gameover[0] == '' or endofcontest[0] == '':
            master.destroy()
            break
            return 0

        unSeulState = retourServeur.split('STATE')
        unSeulState = 'STATE'+unSeulState[1]

        majPlateau(parseState(unSeulState), partie.plateau)

        mesNoeuds = majRoles(partie)

        cellulesEnDangerOuCapturees = calculDangersCapturees(partie, mesNoeuds["rushers"]+mesNoeuds["fournisseurs"]+mesNoeuds["attaquants"])
        cellsDanger = cellulesEnDangerOuCapturees["dangers"]
        cellsCapturees = cellulesEnDangerOuCapturees["capturees"]
        w.delete(ALL)
        affichageGraphique(w)
        w.update_idletasks()
        ##########################################################################################################################################
        for noeud in mesNoeuds["rushers"] :
            IARushers(partie, noeud)
        for noeud in mesNoeuds["fournisseurs"] :
            IAFournisseurs(partie, noeud, cellsDanger)
        IAAttaquants(partie, mesNoeuds, cellsCapturees)
        #---------------------#
        #-------Code IA-------#
        #---------------------#
        
        #IAFournisseurs(partie,mesNoeuds, cellsDanger)
    '''Données utilisables :
            # partie
                partie.plateau
                    partie.plateau["noeuds"]
                    partie.plateau["lignes"]
                        qui sont deux dictionnaires, pour les noeuds, la clé de chaque noeud est son id (en string)
                        pour les lignes, la clé de chaque arete est "idnoeud1;idnoeud2"
                        par exemple pour le noeud d'id 2 : partie.plateau["noeuds"]["2"]
                        par exemple pour l'arete entre le noeud 1 et le noeud 3 : partie.plateau["lignes"]["1;3"]
                                                                                    ou partie.plateau["lignes"]["3;1"]
            # mesNoeuds
                mesNoeuds["rushers"] : liste d'objets noeuds rushers
                mesNoeuds["fournisseurs"] : liste d'objets noeuds fournisseurs
                mesNoeuds["attaquants"] : liste d'objets noeuds attaquants

            # cellsDanger : liste d'objets noeuds qui sont des cellules à nous et en danger

            # cellsCapturees : liste d'objets noeuds qui sont des cellules qui vont se faire capturer si on ne fait rien pour les sauver

        Methodes utilisables :
            # getArete(partie, id1, id2) - retourne l'ojet arete correspondant

            # getNoeud(partie, id) - retourne l'objet noeud correspondant

            # mouv(partie, expediteur, cible, units) - expediteur : objet noeud qui envoi, cible : objet noeud a qui on envoit, units : pourcentage des unités à envoyer

            # dijkstra(partie,noeud1,noeud2) - noeud1 et noeud2 sont des objets noeud - retourne un dictionnaire :
                retour["chemin"] : liste des id des noeuds qui forment le plus court chemin de noeud1 vers noeud2
                    (ex : [1,2,3,4] pour le chemin de 1 à 4 (donc 1 et 4 sont inclus dans cette liste du plus court chemin !) donc liste d'entiers)
                retour["longueur"] : longueur totale du chemin le plus court entre noeud1 et noeud2 (entier donc)
                    ex : 28600
        '''
        #---------------------#
        #-----Fin code IA-----#
        #---------------------#
