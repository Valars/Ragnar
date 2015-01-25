from fonctions_utiles import *
from majListesUtils import *
from getObjects import *
from math import *
from mouv import *
def IARushers(partie,rusher):
    voisins = getVoisins(rusher)
    neutres = []
    for voisin in voisins :
        if voisin.proprio == -1 :
            neutres.append(voisin)


    if len(neutres) > 0 :
        neutres = triLePlusRentable(neutres, rusher)
        mouv(partie, rusher, neutres[0][0],100)