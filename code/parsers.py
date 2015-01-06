import re
from noeud import *
from arete import *
from partie import *
from mouvement import *

'''
parseInit :
prend un parametre (string) : la chaine d'initialisation de la partie envoyée par le serveur
    INIT 20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2]; 1 ; 3CELLS: 1(23,9) ' 2 ' 30 ' 8 ' I ,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I ; 2LINES:1@3433OF2,1@6502OF3
retourne un objet Partie contenant toutes les infos contenues dans la chaine envoyée par le serveur
'''

def parseInit(chaine) :
    partie = Partie()
    noeuds = {}
    lignes = {}

    touteslesinfos = re.findall("INIT(.+)TO[0-9]+\[([0-9]+)\];([0-9]+);[0-9]+CELLS:(.+);[0-9]+LINES:(.+)",chaine)
    touteslesinfos = touteslesinfos[0]

    cells = re.findall("([0-9]+\([0-9]+,[0-9]+\)'[0-9]+'[0-9]+'[0-9]+'[I]+)",touteslesinfos[3])

    for cell in cells :
        infos = re.findall("([0-9]+)\(([0-9]+),([0-9]+)\)'([0-9]+)'([0-9]+)'([0-9]+)'([I]+)",cell)
        noeuds[str(infos[0][0])] = Noeud(int(infos[0][0]), int(infos[0][1]), int(infos[0][2]), int(infos[0][3]), int(infos[0][4]), int(infos[0][5]), infos[0][6], -1, 0, 0, [], "",  {})

    lines = re.findall('[0-9]+@[0-9]+OF[0-9]+',touteslesinfos[4])

    for line in lines :
        infoLigne = re.findall('([0-9]+)@([0-9]+)OF([0-9]+)', line)
        #infoLigne[0][0] = noeud1, 0 2 est le noeud2

        noeud1 = noeuds[infoLigne[0][0]]
        noeud2 = noeuds[infoLigne[0][2]]

        lignes[str(noeud1.id)+";"+str(noeud2.id)] = Arete(noeud1,noeud2,int(infoLigne[0][1]), [])
        lignes[str(noeud2.id)+";"+str(noeud1.id)] = lignes[str(noeud1.id)+";"+str(noeud2.id)]

    partie.plateau = {"noeuds":noeuds,"lignes":lignes}
    partie.matchid = touteslesinfos[0]
    partie.speed = int(touteslesinfos[2])
    partie.me = int(touteslesinfos[1])

    #ajout des informations "aretesConnectees" dans chaque noeud
    for key in partie.plateau["lignes"] :
        if partie.plateau["lignes"][key] not in partie.plateau["lignes"][key].noeud1.aretesConnectees :
            partie.plateau["lignes"][key].noeud1.aretesConnectees.append(partie.plateau["lignes"][key])
            partie.plateau["lignes"][key].noeud2.aretesConnectees.append(partie.plateau["lignes"][key])

    return partie


'''
    STATE<matchid>IS<#players>;<#cells>CELLS:<cellid>[<owner>]<offunits>'<defunits>,...;\
    <#moves>MOVES:<cellid><direction><#units>[<owner>]@<timestamp>'...<cellid>,...


"STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"

<timestamp> en millisecondes, donnée à vitesse x1 : top départ des unités de la cellule source.
<direction> désigne le caractère '>' ou '<' et indique le sens des unités en mouvement en suivant la pointe de flèche.
'''
'''
    prend une chaine Etat telle que retournée par le serveur de l'appel à etat()
    et retourne une liste : des cellules (id,owner,atk,def) et des mouvements (celluleIDFrom,direction[<>],nbUnits,owner,timestamp d'envoi des unités)
'''

def parseState(chaine) :

    cells = re.findall("([0-9]+)\[([0-9]+)\]([0-9]+)'([0-9]+)", chaine)
    moves = re.findall("MOVES:(.*)", chaine)

    if moves != [] :
        moves = moves[0].split(',')

    noeuds = []
    mouvements = []
    for cell in cells :
        noeuds.append({"id":int(cell[0]),"owner":int(cell[1]),"atk":int(cell[2]),"def":int(cell[3])})

    if moves != [] :
        for move in moves :
            arcFrom = re.findall('^([0-9]+)', move)
            arcTo = re.findall("'([0-9]+)$", move)
            arcFrom = int(arcFrom[0])
            arcTo = int(arcTo[0])
            movesSurLarc = re.findall("([<>])([0-9]+)\[([0-9]+)\]@([0-9]+)", move)
            for lemove in movesSurLarc :
                mouvements.append({"from":arcFrom, "to":arcTo, "direction":lemove[0], "nbUnits":int(lemove[1]), "timestamp":int(lemove[3]), "joueur":int(lemove[2])})

    return {"noeuds":noeuds, "moves":mouvements}
