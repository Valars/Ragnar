from tkinter import *
from noeud import *
from arete import *
from partie import *
from parsers import *
from majObjets import *

#simulation du retour serveur
def state() :#                                                                                                                             1
    return "STATE20ac18ab-6d18-450e-94af-bee53fdc8fca IS 2 ; 3CELLS:1[1]12'4,2[2]15'2,3[0]33'6; 4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"




# ################################################
# ################################################
# ################################################



'''
    Affichage dans le canva 'canva' les éléments graphiques contenus dans le plateau 'plateau' (liste des objets noeuds et aretes)
    retourne rien
'''

def initGraphique(canva,plateau, moves) :
    #AFFICHAGE DES LIGNES
    for ligne in plateau["lignes"] :
        noeudDe = ligne.noeud1
        noeudVers = ligne.noeud2
        x,y,x1,y1 = noeudDe.x + noeudDe.radius*20, noeudDe.y+noeudDe.radius*20,noeudVers.x+noeudVers.radius*20,noeudVers.y+noeudVers.radius*20

        ligne.afficher(x,y,x1,y1, w)#affichage de la ligne entre les points qui lui corresponde

    #AFFICHAGE DES NOEUDS
    for noeud in plateau["noeuds"] :
        noeud.afficher(w)

    offsety = 400-15
    for move in moves :
        canva.create_text(120,offsety,text=str(move["joueur"])+"Envoi de "+str(move["from"])+"->"+str(move["to"])+" de "+str(move["nbUnits"])+" unites"+str(move["timestamp"]),font=('Helvetica', 9))
        offsety = offsety-10
# ################################################
# ################################################
# ################################################

#récupération du plateau, à voir si le serveur nous fourni ça d'abord, où si la première chose que notre programme fait est un 'state()'

partie = parseInit("INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(150,10)'2'30'8'I,2(50,200)'2'30'8'II,3(250,200)'2'20'5'I;2LINES:1@3433OF2,1@6502OF3,2@850OF3")

majPlateau(parseState(state()))

#Première récupération de l'état du jeu et mise à jour des cellules / mouvements
etat = parseState(state())

for newInfosNoeud in etat["noeuds"] :
    for noeud in partie.plateau["noeuds"] :
        if newInfosNoeud["id"] == noeud.id :
            #propriétaire des noeuds mis à jour pour 0 si neutre, 1 si à nous, -1 si hostile
            noeud.proprio = 1 if newInfosNoeud["owner"] == partie.me else (0 if newInfosNoeud["owner"] == 0 else -1)

            noeud.off = newInfosNoeud["atk"]
            noeud.defenses = newInfosNoeud["def"]


########################################
########################################
#A ce stade, on possède tous l'état du jeu à l'initialisation !######
########################################
########################################



#affichage graphique du plateau
window = Tk()
w = Canvas(window, width=400, height=400)
initGraphique(w,partie.plateau, etat["moves"])

#BOUCLE PRINCIPALE
while(True) :
    a = input()
    if a == "fin" :
        break
