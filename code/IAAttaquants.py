from fonctions_utiles import *
from mouv import *
from math import *
import time
from getObjects import *

def IAAttaquants(partie, mesNoeuds, cellsCapturees) :
	for attaquant in mesNoeuds["attaquants"] :
		voisins = getVoisins(attaquant)
		voisins = triNoeudsDistances(voisins, attaquant)
		#faire jouer tous nos attaquants
		#tri des cellules qui vont se faire capturées par la distance à attaquant
		cellulesASauver = list(cellsCapturees)
		cellulesASauver = sorted(cellulesASauver, key=lambda dist: dist[0].distances[str(attaquant.id)][1])
		#essayer de sauver un noeud parmis cellsCapturees
		#regarder lequel (faire une rentabilité distance/cout en unités)
		pasEnvoye = False
		for cell in cellulesASauver :
			if cell[0] != attaquant :
				#c'est dans l'ordre du plus proche au plus éloigné de attaquant
				if attaquant.off > cell[1] :
					units = ceil((cell[1]+1)/(attaquant.off)*100) #on envoi ce qu'il faut + 1 unités pour sauver
					mouv(partie, attaquant, cell[0], units)
					pasEnvoye = False
					break
				pasEnvoye = True
		#on a essayé d'envoyer des unités vers une unité à sauver
	#si on n'avait pas assez d'unités, on en envoi les deux tiers de ce qu'on a pour renfort
		if pasEnvoye : #si on pas eu assez d'unités pour pouvoir sauver une unité
			cible = cellulesASauver[0][0]
		else :
			for voisin in voisins :
				if voisin.proprio != -1 and voisin.proprio != attaquant.proprio :
					cible = voisin
					break
		mouv(partie, attaquant, cible, 100)
