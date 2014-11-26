from tkinter import *
from noeud import *
from arete import *
import re

window = Tk()
w = Canvas(window, width=400, height=400)

#simulation du retour serveur
def state() :#                                                                                                                             1
    return "STATE20ac18ab-6d18-450e-94af-bee53fdc8fca IS 2 ; 3CELLS:1[1]12'4,2[2]15'2,3[0]33'6; 4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"


'''prend une chaine en paramètre de la forme suivante :
INIT<matchid>TO<#players>[<me>];<speed>;\
       <#cells>CELLS:<cellid>(<x>,<y>)'<radius>'<offsize>'<defsize>'<prod>,...;\
       <#lines>LINES:<cellid>@<dist>OF<cellid>,...

       <me> et <owner> désignent des numéros de 'couleur' attribués aux joueurs. La couleur 0 est le neutre.
       le neutre n'est pas compté dans l'effectif de joueurs (<#players>).
       '...' signifie que l'on répète la séquence précédente autant de fois qu'il y a de cellules (ou d'arêtes).
       0CELLS ou 0LINES sont des cas particuliers sans suffixe.
       <dist> est la distance qui sépare 2 cellules, exprimée en... millisecondes !
       /!\ attention: un match à vitesse x2 réduit de moitié le temps effectif de trajet d'une cellule à l'autre par rapport à l'indication <dist>.
       De manière générale temps_de_trajet=<dist>/vitesse (division entière).

INIT 20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2]; 1 ; 3CELLS: 1(23,9) ' 2 ' 30 ' 8 ' I ,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I ; 2LINES:1@3433OF2,1@6502OF3

et retourne le matchid, la vitesse du jeu, et la liste des noeuds et des aretes du plateau sous forme de liste d'objets

'''
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
# ################################################
# ################################################
# ################################################



'''
    Affichage dans le canva 'canva' les éléments graphiques contenus dans le plateau 'plateau' (liste des objets noeuds et aretes)
    retourne rien
'''
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
# ################################################
# ################################################
# ################################################

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
def parseEtat(chaine) :
    cells = re.findall("([0-9]+)\[([0-9]+)\]([0-9]+)'([0-9]+)", chaine)
    moves = re.findall("([0-9]+)([<>])([0-9]+)\[([0-9]+)\]@([0-9]+)", chaine)
    noeuds = []
    mouvements = []
    for cell in cells :
        noeuds.append({"id":int(cell[0]),"owner":int(cell[1]),"atk":int(cell[2]),"def":int(cell[3])})
    for move in moves :
        mouvements.append({"celluleFrom":int(move[0]), "direction":move[1], "nbUnits":int(move[2]), "timestamp":int(move[3])})

    return {"noeuds":noeuds, "moves":mouvements}


#récupération du plateau, à voir si le serveur nous fourni ça d'abord, où si la première chose que notre programme fait est un 'state()'
plateau = initPlateau("INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(150,10)'2'30'8'I,2(50,200)'2'30'8'II,3(250,200)'2'20'5'I;2LINES:1@3433OF2,1@6502OF3,2@850OF3")


etat = parseEtat(state())

for newInfosNoeud in etat["noeuds"] :
    for noeud in plateau["noeuds"] :
        if newInfosNoeud["id"] == noeud.id :
            #propriétaire des noeuds mis à jour pour 0 si neutre, 1 si à nous, -1 si hostile
            noeud.proprio = 1 if newInfosNoeud["owner"] == plateau["me"] else (0 if newInfosNoeud["owner"] == 0 else -1)
            noeud.off = newInfosNoeud["atk"]
            noeud.defenses = newInfosNoeud["def"]
########################################
########################################
#A ce stade, on possède tous l'état du jeu à l'initialisation !######
########################################
########################################
'''
    à la disposition : matchid, me, speed, plateau[2] (noeuds) plateau[3] (arêtes)
'''



#affichage graphique du plateau
initGraphique(w,[plateau["noeuds"],plateau["lignes"]])

#BOUCLE PRINCIPALE
while(True) :
    a = input()
    if a == "fin" :
        break
