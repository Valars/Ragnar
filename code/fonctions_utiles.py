# -*- coding: utf-8 -*-

from noeud import * 
from partie import *
from arete import *
from mouvement import *
from getObjects import *
from time import *

'''Nom : tri_mouv_vers_noeud(noeud)

    Description : Cette fonction trie tous les mouvements à destination de noeud dans une liste en fonction du temps restant avant leur arrivée

    E : noeud  : Noeud : Noeud dont on veut les mouvements arrivant sur lui
    
    S : liste  : Liste  : Liste des mouvements triés par ordre croissant sous la forme : [[temps_restant(s), Mouvement],[temps_restant(s), Mouvement],[temps_restant(s), Mouvement]]
'''

def tri_mouv_vers_noeud(noeud):

    time_actuel = etime()               
    liste = []
    
    for arete in noeud.aretesConnectees:

        for mouvement in arete.mouvements:          #pour chaque mouvement autour de noeud
            
            if (mouvement.destination == noeud) :   #Si le mouvement est à destination de noeud
                
                heure_depart = mouvement.timeDepart # alors on calcul le temps restant en millisecondes avant qu'il arrive sur noeud
                temps_necessaire = arete.longueur 
                
                temps_restant = temps_necessaire - (time_actuel - heure_depart)
                
                liste.append([round(temps_restant/1000,3), mouvement])  #on ajoute le mouvement à la liste et on convertie le temps en secondes
                
    liste = sorted(liste, key= lambda temps:  temps[0])     #on effectue le tri sur ordre croissant du temps restant
    
    return liste


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

'''Nom : simulation_noeud(noeud, mouvement_theorique = None)
    
    Description : Cette fonction effectue la simulation de résolution des mouvement à destination de noeud. Il est possible de rajouter un faux mouvement qui sert
                    a trouver par exemple le nombre minimal d'unités à envoyer sur le noeud pour le capturer ou pour le proteger contre une attaque imminente par exemple
    
    E : noeud        : Noeud : Noeud que l'on souhaite simuler
    
    S : noeud_cible  : Dictionnaire  : Dictionnaire contenant les résultats de la simulation sous la forme {"atk": Int, "def": Int, "maxAtk" : Int, "maxDef" : Int, "prod" : float, "proprio" : Int}
'''

def simulation_noeud(noeud, mouvement_theorique = None):
    liste_mouv = tri_mouv_vers_noeud(noeud)  #Recuperation des mouvement triés vers noeud 

    if(mouvement_theorique != None):    #Si un faux mouvement pour test a été ajouté

        i = 0
        insertion_faite = False
    
        while(i < len(liste_mouv) and insertion_faite == False):    #Ajout du faux mouvement dans la liste triée
        
            if(liste_mouv[i][0] >= mouvement_theorique[0]):
                liste_mouv.insert(i, mouvement_theorique)
                insertion_faite = True
            elif(i == len(liste_mouv)-1):
                liste_mouv.append(mouvement_theorique)
                insertion_faite = True
                
            i+=1
    
    #On crée un dictionnaire avec les infos utiles du noeud cible pour pouvoir les modifier à volonté pendant la simulation
    noeud_cible =  {"atk" : noeud.off, "def" : noeud.defenses, "maxAtk" : noeud.offsize, "maxDef" : noeud.defsize, "prod" : noeud.prod, "proprio" : noeud.proprio}
    
    time_precedent = 0                          #T-1 (utile pour le calcul de la production) 
        
    report_prod_atk = 0                         #Si production non entiere entre T-1 et T, on stock dans ces variables pour les reconsidérer plus tard
    report_prod_def = 0                        
    
    for couple in liste_mouv:           #Pour chaque couple de donnée tempsrestant/mouv dans la liste
            
        if ( noeud_cible["proprio"] != -1) :            #Si le noeud n'est pas neutre on calcul la production de l'attaque et de la défense du noeud

            prod_atk = (couple[0] - time_precedent) * noeud_cible["prod"] + report_prod_atk
            report_prod_atk = +prod_atk % 1   #Stockage de la partie décimale
            
            noeud_cible["atk"] += int(prod_atk)
            noeud_cible["atk"] = min([noeud_cible["atk"] , noeud_cible["maxAtk"]]) #Verification que l'ajout de la production ne fasse pas dépasser la limite d'atk du noeud

            prod_def =  couple[0] - time_precedent + report_prod_def
            report_prod_def = prod_def % 1
            noeud_cible["def"] += int(prod_def) 
            noeud_cible["def"] = min([noeud_cible["def"] , noeud_cible["maxDef"]])
            
        time_precedent  = couple[0]
        
        if(couple[1].joueur == noeud_cible["proprio"]): #si le mouvement qui arrive est un renfort
            
            noeud_cible["atk"] += couple[1].nbUnites
            noeud_cible["atk"] = min([noeud_cible["atk"] , noeud_cible["maxAtk"]])
            
        else: #si le mouvement qui arrive est une attaque 

            noeud_cible["def"] -= couple[1].nbUnites    #on retire nb unit du mouvement à la défense du noeud
            
            if(noeud_cible["def"] < 0) :     #si l'attaque rend la défense du noeud négative
                
                noeud_cible["atk"] -= abs(noeud_cible["def"]) #alors cela veut dire que la défence a été détruite et que cette valeur négative doit s'appliquer aux unités d'attaque du noeud
                
                noeud_cible["def"] = 0 #et on passe la défence à 0
                
                if(noeud_cible["atk"] < 0) :    #si, l'atk de la cible est au final elle aussi négative, cela veut dire que le noeud à été capturé
                    
                    noeud_cible["atk"] = min([abs(noeud_cible["atk"]), noeud_cible["maxAtk"]])    #on fait donc l'absolue du nombre d'unités attaquantes 
                    noeud_cible["proprio"] = couple[1].joueur       #et le nouveau proprio est le joueur à qui appartenait les unités d'attaque
                    report_prod_atk = 0         #Reset des variables de report des parties décimales des production, en effet, au changement de propriétaire
                    report_prod_def = 0         #Toute production est remise à 0
        
    return noeud_cible
    
'''Nom : doitEnvoyer(partie, noeud1, noeud2)

    Description : Cette fonction permet de déterminer avec une fiabilité élevée le nombre minimal d'unités nécessaires à la capture d'un noeud à un instant t 
                    via une simulation prendant en compte les mouvements en cours, les changements de propriétaire du noeud dans le temps etc...
                    
    
    E : partie  : Partie : Objet de la partie en cours
        noeud1  : Noeud  : Noeud qui doit envoyer les unités
        noeud2  : Noeud  : Noeud dont on veut savoir combien d'unité il faut pour la capturer
    
    S :         : Int   : Nombre d'unités nécessaires à la capture du noeud2 
'''

def doitEnvoyer(partie, noeud1, noeud2):
    
    simu = simulation_noeud(noeud2)         #On effectue une premiere simulation pour déterminer la résolution des mouvements autour de noeud2

    temps_restant_mouv = round((getArete(noeud1, noeud2).long /1000), 3)    #On met en place un faux mouvement qui servira de test pour déterminer le nombre d'unités à envoyer pour capturer le noeud
    test_nbUnites = 0           
    test_mouv = [temps_restant_mouv,Mouvement(noeud2,test_nbUnites,etime(),noeud1.proprio)]

    resultat_valide = False                 #Boolean de sortie de boucle

    while(resultat_valide == False):        #Tant que les simulations ne ressortent pas un résultat satisfaisant
        
        if(simu["proprio"] == noeud1.proprio):  #Si à la fin de la simulation noeud2 nous appartient

            if(test_mouv[1].nbUnites == 0):     #si on a pas eu besoin d'utiliser le faux mouvement pour capturer le noeud alors on a pas besoins d'envoyer quelque unités que ce soit
                resultat_valide = True
            
            elif(simu["atk"] > 1 and test_moub[1].nbUnites > 1): #Si au final le noeud capturé a plus d'une unités offensives, et le faux mouvement aussi, alors on doit il existe peut etre un nombre d'unités d'attaque plus faible qui puisse permettre la capture du noeud, or on charche le nombre minimal d'unités
                test_mouv[1].nbUnites -= 1                  #On décremente le nombre d'unités dans le faux mouvement de 1 puis on resimule
                simu = simulation_noeud(noeud2, test_mouv)  
                
            else :      #Sinon, c'est à dire que l'on a trouvé le nombre minimal d'unité pour capturer le noeud avec un minimum d'unités (le noeud n'a au final que 0 ou une unité d'attaque de dispo)
                resultat_valide = True
    
        else:       #Si à la fin de la simulation le noeud ne nous appartient pas

            if(test_mouv[1].nbUnites == 0 and (simu["atk"]+simu["def"]) > 0): #Si le faux mouvement n'a pas encore été utilisé en simulation (nbUnites = 0) et que le noeud a plus que 0 unités d'attaque dispo
                test_mouv[1].nbUnites = simu["atk"]+simu["def"] #alors on ressimule avec le faux mouvement qui dispose d'autant d'unités d'attaque que le noeud n'a d'unités d'attaque et de défense
                simu = simulation_noeud(noeud2, test_mouv)

            elif(simu["atk"]+simu["def"] >= 0 ):    #En revanche si le faux mouvement a déja été utilisé alors on reteste en incrémentant son nbUnites jusqu'à ce que le simulation nous donne le résultat escompté
                test_mouv[1].nbUnites += 1
                simu = simulation_noeud(noeud2, test_mouv)
                
    #Résumé des cas à la fin de la simulation :
    #Le noeud nous appartient 
    #   - Et nous n'avons pas encore estimer de mouvement nécessaires pour le capturer (donc nos alliés n'ont pas besoin de noeud pour capturer le noeud)
    #       - On renvoi 0 unités nécessaire pour capturer
    #   - Et le noeud a un nombre d'unités superieur à 1 et le mouvement rajouté à la simulation à aussi plus d'une unité (donc on doit pouvoir réduire ce nombre)
    #       - On décremente le nb d'unités dans le mouvement de test et on ressimule
    #   - Sinon (Soit le mouvement suplémentaire permet la capture avec une seule unité, soit le noeud n'a que une unité d'attaque donc on a le mouvement min pour la capture)
    #       - On a trouvé le nombre minimal d'unités pour capturer noeud2, on sort de la fonction
    #
    #Le noeud ne nous appartient pas
    #   - Et on a pas encore simulé avec le rajout d'un mouvement 
    #       -On simule à nouveau en créant le mouvement de test avec un nombre d'unités valant la défense plus l'attaque du noeud2
    #   - Et on a déja fait une simulation en rajoutant un mouvement de test
    #       - On incrémente le nombre d'unités du mouvement et on relance la simulation
    
    
    return test_mouv[1].nbUnites #On renvoie le nombre minimal d'unités requis pour capturer le noeud

'''Nom : peutCapturer(partie, noeud_attaquant, noeud_defenseur)

    Description : Cette fonction permet de déterminer si un noeud est capable de capturer un voisin
    
    E : partie  : Partie : Objet de la partie en cours
        noeud_attaquant  : Noeud : Noeud dont on veut savoir si il peut capturer noeud_defenseur
        noeud_defenseur  : Noeud : Noeud dont on veut savoir si il peut etre capturé par noeud_attaquand
    
    S : reponse : Int    : Tableau : [True/False, nombre d'unités à envoyer au min pour capturer] 
'''

def peutCapturer(partie, noeud_attaquant, noeud_defenseur):
    
    capacite_off = peutEnvoyer(noeud_attaquant)

    units_necessaires = doitEnvoyer(partie,noeud_attaquant, noeud_defenseur)
    
        
    if(capacite_off > units_necessaires): reponse = True
        
    else : reponse = False
    
    return [reponse, units_necessaires]
    
'''Nom : triNoeudsDistances(listeNoeud, noeudDistant)

    Description : Cette fonction renvoie une liste de noeuds triés par leur distance par rapport à noeudDistant
    
    E : listeNoeud   : Liste : Liste des noeud à classer selon leur distance à noeudDistant
        noeudDistant : Noeud : Noeud par rapport auquel on trie les autres noeuds
    
    S : maListe      : Liste : Liste des noeuds triés du plus proche au plus éloigné
'''    
def triNoeudsDistances(listeNoeuds, noeudDistant) :
    print("debut du tri")
    maliste = list(listeNoeuds)
    maliste = sorted(maliste, key=lambda dist: dist.distances[str(noeudDistant.id)][1])
    print("fin du tri")
    return maliste
   
'''Nom : triLePlusRentable(listeNoeud, noeudDistant)

    Description : Cette fonction renvoie une liste contenant les mêmes noeud que le premier paramètre mais triés en fonction de 
                    la rentabilité de chaque noeud par rapport au noeud distant, par exemple, pour un fournisseur, on passe les noeuds
                    en danger en tant que premier parametre et on saurait quelle noeud en danger est le plus important à aider par
                    rapport à ce fournisseur. La liste renvoyée est une liste de listes contenant deux éléments, le premier le Noeud en 
                    danger et le second sa rentabilité, plus la valeur de la rentabilité est elevée, plus le noeud est important.
    
    E : listeNoeud   : Liste : Liste des noeud à classer selon leur rentabilité
        noeudDistant : Noeud : Noeud qui sert de point de réference pour le calcul de la rentabilité des autres noeuds
    
    S : listeTrie    : Liste : [[rentabilite, noeud],[rentabilite, noeud],[rentabilite, noeud]...] du noeud le plus rentable au moins rentable
'''
def triLePlusRentable(listeNoeud, noeudDistant ):
    
    listeTrie = []
    
    for noeud1 in listeNoeud:
        noeud1Score = 0
        
        for noeud2 in listeNoeud:
            
            if (noeud1 != noeud2):
                
                marge = max([noeud1.prod, noeud2.prod]) - min([noeud1.prod, noeud2.prod])
                diffDistance = getDistance(noeudDistant, noeud1) - getDistance(noeudDistant, noeud2)
            
                if (diffDistance > 0):
                    noeudLoin = noeud1
                    noeudProche = noeud2
                    
                else:
                    noeudLoin = noeud2
                    noeudProche = noeud1
                    
                if(diffDistance == 0):
                    if(noeud1.prod > noeud2.prod): noeud1Score += 1
                    
                elif (diffDistance <= (getDistance(noeudDistant, noeudProche) * marge)):
                    if(noeudLoin == noeud1) : noeud1Score += 1
                    
                else: 
                    if(noeudProche == noeud1) : noeud1Score += 1
                    
        listeTrie.append([noeud1, noeud1Score])
                    
    
    listeTrie = sorted(listeTrie, key=lambda rentabilite:rentabilite[1])
        
    return listeTrie    
    
'''Nom : besoinUnitesDanger(cellsDanger, noeud):

    Description : Cette fonction recherche le noeud dans la liste rentrée (cellsDanger, cf. ragnar.py) et renvoie le nb correspondant
    d'unité nécessaires pour la sauver
    
    E : cellsDanger    : Liste : Liste des noeuds en danger
        cellsDanger    : Noeud : Noeud pour lequel on veut connaitre le nombre d'unités nécessaires pour le sortir du danger
    
    S : nbUnitesRequis : Int   : Vaut 0 si jamais le noeud rentré n'était pas dans cellsDanger
'''
def besoinUnitesDanger(cellsDanger, noeud):
    
    trouve = False
    i = 0
    nbUnitesRequis = 0
    while (trouve == False and i != len(cellsDanger)):
        if(cellsDanger[i][0].id == noeud.id):
            trouve = True
            nbUnitesRequis = cellsDanger[i][1]
    
    return nbUnitesRequis
    
    

    
    