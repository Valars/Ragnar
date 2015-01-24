from fonctions_utiles import *
from majListesUtils import *
from getObjects import *
from math import *


def IARushers(partie,rusher,cellsDanger):
    listeNeutreDegre1 = [] #liste des neutres de degre 1
    listeNeutresaCapturer = [] #liste des neutre a capturer
    
    if rusher not in cellsDanger:
        for voisin in getVoisins(rusher):
            if voisin.proprio == -1 :
                diff = peutCapturer(partie,rusher,voisin)
                if diff[0] == True : #si le rusher peut capturer le voisin
                    if len(voisin.aretesConnectees) == 1 : #si le voisin est de degre 1
                        listeNeutreDegre1.append([voisin,diff[1]])
                    else :
                        listeNeutresaCapturer.append([voisin,diff[1]])#ajouter a la liste des neutres à capturer et diff
                        
            if len(listeNeutreDegre1) > 0 : #si nous avons des neutres de degre 1
                if len(listeNeutreDegre1) > 1 : #si cette liste à plus dun element
                    noeud_rentableDeDeg1 = triLePlusRentable(listeNeutreDegre1,rusher)
                    a_envoyer = ceil((noeud_rentableDeDeg1[0][1]/rusher.atk)*100) #noeud_rentableDeDeg1[0][1] recupere le besoin du noeud le plus rentable
                    mouv(partie, rusher, noeud_rentableDeDeg1[0][0], a_envoyer)
                    return
                else : #sinon nous avons qun seul noeud 
                    besoin = peutCapturer(partie,cellsDanger, voisin)
                    a_envoyer = ceil((besoin[1]/rusher.atk)*100)
                    mouv(partie, rusher, voisin, a_envoyer)
                    return
            else : #sinon les neutres ne sont pas de degre un 
                
                if len(listeNeutresaCapturer) > 1 : #si nous avons plus dun noeud, un tri du plus rentables est necessaire
                    noeud_rentableNotDeg1 = triLePlusRentable(listeNeutresaCapturer,rusher)
                    a_envoyer = ceil((listeNeutresaCapturer[0][1]/rusher.atk)*100)
                    mouv(partie, rusher, noeud_rentableNotDeg1[0][0], a_envoyer)
                    return
                else :
                    besoin = peutCapturer(partie,cellsDanger, voisin)
                    a_envoyer = ceil((besoin[1]/rusher.atk)*100)
                    mouv(partie, rusher, voisin, a_envoyer)
                    return
    pass        