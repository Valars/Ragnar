from noeud import * 
from partie import *
from arete import *
from mouvement import *
from getObjects import *
'''Nom : peutEnvoyer(noeud)
    Description : Cette fonction permet de connaitre le nombre d'unité disponible sur un noeud pour un mouvement.
                    Les mouvements offensifs vers ce noeud sont déduis afin de limiter le risque de capture du noeud
                    en cas d'envoi d'un nombre trop important d'unités ne permettant plus de défendre contre l'attaque en cours.
    
    E : noeud  : Noeud : Noeud dont on veut savoir le nombre d'unités disponible pour un mouvement
    
    S : total  : Int  : Total des unités disponibles à l'attaque
'''

def peutEnvoyer(noeud):
    
    total = noeud.off
    
    for arete in noeud.aretesConnectees:
        for mouvement in arete.mouvements:
            if (mouvement.proprio != noeud.proprio and mouvement.destination == noeud.id):
                total -= mouvement.nbUnites
    
    if (total < 0) : total = 0
    
    return total

'''Nom : doitEnvoyer(partie, noeud_attaquant, noeud_defenseur)

    Description : Cette fonction permet de connaitre le nombre d'unité disponible sur un noeud pour un mouvement.
                    Les mouvements offensifs vers ce noeud sont déduis afin de limiter le risque de capture du noeud
                    en cas d'envoi d'un nombre trop important d'unités ne permettant plus de défendre contre l'attaque en cours.
    
    E : partie  : Partie : Objet de la partie en cours
        noeud_attaquant  : Noeud : Noeud qui doit envoyer les unités
        noeud_defenseur  : Noeud : Noeud dont on veut savoir combien d'unité il faut pour la capturer
    
    S : a_envoyer  : Int  : Nombre d'unités nécessaire pour capturer le noeud défenseur depuis le noeud attaquant
'''
def doitEnvoyer(partie, noeud_attaquant, noeud_defenseur):
    
    total_noeud_off = noeud_defenseur.off     #total des unités dispos dans le noeud + production + renfort en cours
    total_noeud_def = noeud_defenseur.defensives   #total des unites deff dispos + production
    total_from_us = 0
    total_from_other = 0
    a_envoyer = 0
    
    for arete in noeud_defenseur.aretesConnectees:
        for mouvement in arete.mouvements :
            
            if (mouvement.destination == noeud_defenseur.id):
                
                if (mouvement.joueur == noeud_defenseur.proprio) :
                    total_noeud += mouvement.nbUnites
                elif (mouvement.joueur == partie.me) :
                    total_from_us += mouvement.nbUnites
                else :
                    total_from_other += mouvement.nbUnites
            
            if (mouvement.destination == noeud_attaquant.id and ):
                total_noeud += mouvement.nbUnites
    
    if(noeud_defenseur.proprio != -1):
        if(total_noeud - noeud_defenseur.defensives != 30):
        arete_entre_noeuds = getArete(partie, noeud_attaquant.id, noeud_defenseur.id)
        total_noeud += arete_entre_noeuds.longueur / 1000 * (noeud_defenseur.prod) #Ajout de la production des noeud attaquants durent le trajet
        
    #ajouter les unités produites par le noeud défenseur pendant le trajet
        #unités offensive produites = arete.taille/1000* production_attaque
        
        #unités def produites = arete.taille/1000 * production_defense (?????)
        #considerer les limites de 30 unites attaquantes dans un noeud et 8 pour la défense
        
    a_envoyer = abs(total_noeud - total_from_other) - total_from_us        
    if (a_envoyer < 0) : a envoyer = 0
    
    return a_envoyer


'''Nom : peutCapturer(partie, noeud_attaquant, noeud_defenseur)

    Description : Cette fonction permet de déterminer si un noeud est capable de capturer un voisin
    
    E : partie  : Partie : Objet de la partie en cours
        noeud_attaquant  : Noeud : Noeud qui envisage d'attaquer
        noeud_defenseur  : Noeud : Noeud qui pourrait etre attaqué
    
    S : reponse : Int    : Tableau : [True/False, nombre d'unités à envoyer au min pour capturer] 
'''

def peutCapturer(partie, noeud_attaquant, noeud_defenseur):
    
    capacite_off = peutEnvoyer(noeud_attaquant)
    units_necessaires = doitEnvoyer(partie, noeud_attaquant, noeud_defenseur)
    
        
    if(capacite_off > units_necessaires): reponse = True
        
    else : reponse = False
    
    return [reponse, units_necessaires]

