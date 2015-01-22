from fonctions_utiles import *
from majListesUtils import *
from getObjects import *
from math import *

def IARushers(partie,rusher,cellsDanger):
    listeDegre1 = [] #liste des noeuds de degre 1
    listeNeutreDegre1 =[] #liste des noeutres de degre 1
    if rusher not in cellsDanger:
        for voisin in getVoisins(rusher):
            if voisin["proprio"]==-1:
                diff = doitEnvoyer(partie,rusher,voisin)
                if diff > 0 and peutEnvoyer(rusher) > diff:
                    if len(voisin.aretesConnectees) == 1 :
                         append.listededegré1(voisin)
                         diff
                    else :
                        append.li#ajouter a la liste des neutres à capturer et diff
        
        if len(listedesneutresdedegré1) > 0 :
            if len(listedesneutresdedegré1) > 1 :
               noeud_rentableDeDeg1 = triLePlusRentable(listedesneutresdedegré1,rusher)
               peutEnvoyer(noeud_rentableDeDeg1)
               return
            else :
                envoyer au seul neutre de degré 1
                return
        else :
            si len(listeDesAutresNeutres) > 1
                noeud_rentableDeDeg1 = triLePlusRentable(listedesneutresdedegré1,rusher)
                envoyer vers ce noeud
                return
            sinon :
                envoyer au seul neutre de la liste
                return
    pass        