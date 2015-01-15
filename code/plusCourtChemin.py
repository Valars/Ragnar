from getObjects import *
from partie import *
from noeud import *
import time
'''
    Nom : dijkstra (partie, de, vers)

    E : partie : Partie : L'objet partie, qui contient le plateau de jeu
        de     : Noeud  : Noeud d'origine, début du chemin
        vers   : Noeud  : Noeud de fin, d'arrivée du chemin

    S:         : Liste  :  un dictionnaire à deux indices :
                            "chemin" :      liste des id des noeuds parcourus étant sur le chemin le plus court du noeud 'de' vers le noeud 'vers'
                            "longueur" :    distance totale entre le noeud 'de' et le noeud 'vers' sur le chemin le plus court
'''

def dijkstra(partie, de, vers) :

    # Initialisations :
    infinity = float("inf")
    distances = {} #liste des distances sous la forme "1":4700, "2":4800
    nonParcourus = dict(partie.plateau["noeuds"]) #noeuds pas encore parcourus (est vidé petit à petit pour chaque noeud parcouru)
    precedences = {} #liste des précédences des noeuds pour les plus courts chemins
    
    # Initialisation des distances à +infinity pour tous les noeuds
    # Initialisation des précédences à 0 pour tous les noeuds
    for cle in partie.plateau["noeuds"] :
        distances[str(partie.plateau["noeuds"][cle].id)] = infinity
        precedences[str(partie.plateau["noeuds"][cle].id)] = 0
    # On met la distance du noeud dont on part à 0 :)
    distances[str(de.id)] = 0

    # Tant qu'on a pas parcouru tous nos noeuds

    while nonParcourus :#len(nonParcourus) != 0:

        # Récupérer le noeud ayant la distance la plus petite positive
        tmp = dict(nonParcourus)

        # Récupérer le noeud ayant la distance la plus petite positive :
        idNoeudMin, distMin = None, infinity
        for key in tmp :
            if (distances[key] < distMin) :
                distMin = distances[key]
                idNoeudMin = key
        
        aParcourir = getNoeud(partie, idNoeudMin)
        # Enlever aParcourir de nonParcourus
        del nonParcourus[str(aParcourir.id)]

        # Pour chaque voisin de aParcourir :
        voisins = getVoisins(aParcourir)
        for voisin in voisins :
            
            nouvelle_distance = distances[str(aParcourir.id)] + partie.plateau["lignes"][str(aParcourir.id)+";"+str(voisin.id)].longueur
            if distances[str(voisin.id)] > nouvelle_distance:
                distances[str(voisin.id)] = nouvelle_distance
                precedences[str(voisin.id)] = aParcourir.id

    chemin = []
    n = vers.id
    while n != de.id :
        chemin.append(n)
        n = precedences[str(n)]
    chemin.append(de.id)

    chemin.reverse()

    return {"chemin" : chemin, "longueurs" : distances}

'''
    Nom : calc_distance() (partie, noeud)

    E : partie : Partie : L'objet partie, qui contient le plateau de jeu
        noeud     : Noeud  : Noeud pour lequel on veut déterminer le plus court chemin vers les autres noeuds

'''

def initialisationDistances(partie) :
    """Initialisation des dictionnaires de distances de chacun des noeuds à la valeur None"""
    initity, init = float("inf"), {}
    
    for noeud in partie.plateau["noeuds"] : # Création du dictionnaire de distances initialisé à None pour chacune de ses clefs
        init[noeud] = None
    
    for noeud in partie.plateau["noeuds"] : # On affecte ce dictionnaire à chacun des noeuds du graphe
        partie.plateau["noeuds"][noeud].distances = dict(init)

def calc_distances(partie):
    """Pour chaque noeud du graphe on va déterminer le plus court chemin vers chacun des autres noeuds
        On conserve pour chaque noeud la distance total à parcourir vers sa cible, ainsi que
        le noeud le plus proche pour y parvenir """
        
    initialisationDistances(partie)
    
    for noeud_debut in partie.plateau["noeuds"]: 
        for noeud_fin in partie.plateau["noeuds"][noeud_debut].distances:
            # Si le plus court chemin entre deux noeuds différents n'est pas défini, 
            # on utilise l'algorithme de Dijkstra pour le déterminer
            if partie.plateau["noeuds"][noeud_debut].distances[noeud_fin] == None and noeud_debut != noeud_fin : 
                plus_court = dijkstra(partie, getNoeud(partie,noeud_debut), getNoeud(partie,noeud_fin))
                
                # A partir du plus court chemin entre noeud_debut et noeud_fin, on procède à une 
                # analyse de la liste des noeuds parcourus, pour en déduire les plus courts chemins 
                # existants entre les noeuds intermédiaires
                # Ex : Du plus court chemin de A à D (A-B-C-D) nous en déduisons
                # Le plus court chemin de {A-A, A-B, A-C, A-D, B-A, B-B, B-C, B-D, C-A, C-B, C-C, C-D, D-A, D-B, D-C, D-D}
                
                for i in range(len(plus_court["chemin"])) : 
                    for j in range(len(plus_court["chemin"])) :
                    
                        # Analyse du parcours séquentiel de "Chemin"
                        if (j > i) : # Si noeud_f est à droite de noeud_d, noeudPlusProche est le voisin de droite de noeud_d
                            noeudPlusProche = plus_court["chemin"][i+1]
                        elif (j < i) :# Si noeud_f est à gauche de noeud_d, noeudPlusProche est le voisin de gauche de noeud_d
                            noeudPlusProche = plus_court["chemin"][i-1]
                        else : # Si noeud_f est noeud_d, alors noeudPlusProche est noeud_d
                            noeudPlusProche = plus_court["chemin"][i]
                        
                        noeud_d, noeud_f, noeudPlusProche  = str(plus_court["chemin"][i]), str(plus_court["chemin"][j]), str(noeudPlusProche)
                        dist = max(plus_court['longueurs'][noeud_d], plus_court['longueurs'][noeud_f]) - min(plus_court['longueurs'][noeud_d], plus_court['longueurs'][noeud_f])
                        partie.plateau["noeuds"][noeud_d].distances[noeud_f] = [noeudPlusProche, dist]

