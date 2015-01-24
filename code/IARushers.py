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

    neutres = triLePlusRentable(neutres, rusher)
    try :
        mouv(partie, rusher, neutres[0][0],100)
    except Exception :
        pass