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
		if len(cellulesASauver) > 0 :
			cellulesASauver = sorted(cellulesASauver, key=lambda dist: dist[0].distances[str(attaquant.id)][1])
			for cell in cellulesASauver :
				if attaquant != cell[0] :
					print("####################")
					print("attaquant : "+str(attaquant.id)+" | cible : "+str(cell[0].id))
					print(attaquant.distances[str(cell[0].id)][0][0])
					print("####################")
					#time.sleep(10000)
					mouv(partie, attaquant, getNoeud(partie,attaquant.distances[str(cell[0].id)][0]),50)
					break
		for voisin in voisins :
			if voisin.proprio != -1 and voisin.proprio != attaquant.proprio :
				mouv(partie, attaquant, voisin,100)