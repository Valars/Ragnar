# -*- coding: utf-8 -*-


"""Robot-joueur de Pooo

    Le module fournit les fonctions suivantes :
        register_pooo(uid)
        init_pooo(init_string)
        play_pooo()


"""

## chargement de l'interface de communication avec le serveur
#from poooc import order, state, state_on_update, etime

# mieux que des print partout
import logging
# pour faire de l'introspection
import inspect
from arete import *
from noeud import *

def initPlateau(chaine) :
    noeuds = []
    lignes = []

    touteslesinfos = re.findall("INIT(.+)TO[0-9]+\[([0-9]+)\];([0-9]+);[0-9]+CELLS:(.+);[0-9]+LINES:(.+)",chaine)
    touteslesinfos = touteslesinfos[0]

    cells = re.findall("([0-9]+\([0-9]+,[0-9]+\)'[0-9]+'[0-9]+'[0-9]+'[I]+)",touteslesinfos[3])
    for cell in cells :
        infos = re.findall("([0-9]+)\(([0-9]+),([0-9]+)\)'([0-9]+)'([0-9]+)'([0-9]+)'([I]+)",cell)
        noeuds.append(Noeud(int(infos[0][0]), int(infos[0][1]), int(infos[0][2]), int(infos[0][3]), int(infos[0][4]), int(infos[0][5]), infos[0][6]))

    lines = re.findall('[0-9]+@[0-9]+OF[0-9]+',touteslesinfos[4])

    for line in lines :
        infoLigne = re.findall('([0-9]+)@([0-9]+)OF([0-9]+)', line)
        lignes.append(Arete(int(infoLigne[0][0]), int(infoLigne[0][2]), int(infoLigne[0][1])))

    return {"matchid":touteslesinfos[0], "speed":int(touteslesinfos[2]),"noeuds":noeuds,"lignes":lignes,"me":int(touteslesinfos[1])}

def parseEtat(chaine) :
    cells = re.findall("([0-9]+)\[([0-9]+)\]([0-9]+)'([0-9]+)", chaine)
    moves = re.findall("MOVES:(.*)", chaine)
    moves = moves[0].split(',')

    noeuds = []
    mouvements = []
    for cell in cells :
        noeuds.append({"id":int(cell[0]),"owner":int(cell[1]),"atk":int(cell[2]),"def":int(cell[3])})

    for move in moves :
        arcFrom = re.findall('^([0-9]+)', move)
        arcTo = re.findall("'([0-9]+)$", move)
        arcFrom = int(arcFrom[0])
        arcTo = int(arcTo[0])
        movesSurLarc = re.findall("([<>])([0-9]+)\[([0-9]+)\]@([0-9]+)", move)
        for lemove in movesSurLarc :
            mouvements.append({"from":arcFrom, "to":arcTo, "direction":lemove[0], "nbUnits":int(lemove[1]), "timestamp":int(lemove[3]), "joueur":int(lemove[2])})

    return {"noeuds":noeuds, "moves":mouvements}


#création d'un objet partie pour stocker userID matchID, et plateau :)
global laPartie = partie()

def register_pooo(uid):
    """Inscrit un joueur et initialise le robot pour la compétition

        :param uid: identifiant utilisateur
        :type uid:  chaîne de caractères str(UUID)

        :Example:

        "0947e717-02a1-4d83-9470-a941b6e8ed07"

    """
    laPartie.uid = uid

def initGraphique(canva,plateau) :
    #AFFICHAGE DES LIGNES
    for ligne in plateau[1] :
        noeudDe = plateau[0][ligne.de-1]
        noeudVers = plateau[0][ligne.vers-1]
        x,y,x1,y1 = noeudDe.x + noeudDe.radius*20, noeudDe.y+noeudDe.radius*20,noeudVers.x+noeudVers.radius*20,noeudVers.y+noeudVers.radius*20

        ligne.afficher(x,y,x1,y1, w)#affichage de la ligne entre les points qui lui corresponde

    #AFFICHAGE DES NOEUDS
    for noeud in plateau[0] :
        noeud.afficher(w)

def init_pooo(init_string):
    """Initialise le robot pour un match

        :param init_string: instruction du protocole de communication de Pooo (voire ci-dessous)
        :type init_string: chaîne de caractères (utf-8 string)


       INIT<matchid>TO<#players>[<me>];<speed>;\
       <#cells>CELLS:<cellid>[<owner>]<x>'<y>'<radius>'<offsize>'<defsize>'<prod>,...;\
       <#lines>LINES:<cellid>@<dist>OF<cellid>,...

       <me> et <owner> désignent des numéros de 'couleur' attribués aux joueurs. La couleur 0 est le neutre.
       le neutre n'est pas compté dans l'effectif de joueurs (<#players>).
       '...' signifie que l'on répète la séquence précédente autant de fois qu'il y a de cellules (ou d'arêtes).
       0CELLS ou 0LINES sont des cas particuliers sans suffixe.
       <dist> est la distance qui sépare 2 cellules, exprimée en... millisecondes !
       /!\ attention: un match à vitesse x2 réduit de moitié le temps effectif de trajet d'une cellule à l'autre par rapport à l'indication <dist>.
       De manière générale temps_de_trajet=<dist>/vitesse (division entière).

        :Example:

        "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;2CELLS:1[2]23'9'2'30'8'1,2[1]41'55'1'30'8'2;2LINES:1@3433OF2,1@6502OF3"

    """
    laPartie.plateau = initPlateau(init_string)
    laPartie.matchid = laPartie.plateau["matchid"]
    laPartie.speed = laPartie.plateau["speed"]
    laPartie.me = laPartie.plateau["me"]
    laPartie.plateau = [laPartie.plateau["noeuds"],laPartie.plateau["lignes"]]



def play_pooo():
    """Active le robot-joueur

    """
    logging.info('Entering play_pooo fonction from {} module...'.format(inspect.currentframe().f_back.f_code.co_filename))
    etat = parseEtat(state())
    ### Début stratégie joueur ###
    # séquence type :
    # (1) récupère l'état initial
    # init_state = state()
    # (2) TODO: traitement de init_state
    # (3) while True :
    # (4)     state = state_on_update()
    # (5)     TODO: traitement de state et transmission d'ordres order(msg)
    window = Tk()
    w = Canvas(window, width=400, height=400)
