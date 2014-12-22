from getObjects import *

'''
    dijkstra(partie,de,vers)
    Entrées :
        partie :    l'objet partie, qui contient le plateau de jeu
        de :        un objet noeud duquel on part
        vers :      un objet noeud, vers lequel on va

    Sorties :
        un dictionnaire à deux indices :
            "chemin" :      liste des id des noeuds parcourus étant sur le chemin le plus court du noeud 'de' vers le noeud 'vers'
            "longueur" :    distance totale entre le noeud 'de' et le noeud 'vers' sur le chemin le plus court
'''

def dijkstra(partie, de, vers) :
    #initialisations
    distances = {} #liste des distances sous la forme "1":4700, "2":4800
    nonParcourus = dict(partie.plateau["noeuds"]) #noeuds pas encore parcourus (est vidé petit à petit pour chaque noeud parcouru)
    precedences = {} #liste des précédences des noeuds pour les plus courts chemins
    #initialisation des distances à -1 pour tous les noeuds
    #initialisation des précédences à 0 pour tous les noeuds
    for cle in partie.plateau["noeuds"] :
        distances[str(partie.plateau["noeuds"][cle].id)] = -1
        precedences[str(partie.plateau["noeuds"][cle].id)] = 0
    #on met la distance du noeud dont on part à 0 :)
    distances[str(de.id)] = 0

    #tant qu'on a pas parcouru tous nos noeuds
    while nonParcourus != {} :
        #récupérer le noeud ayant la distance la plus petite positive
        distMin = -1
        aParcourir = None
        for cle in distances :
            if distances[cle] >= 0 and distMin < distances[cle] :
                distMin = distances[cle]
                aParcourir = getNoeud(partie, int(cle))
        #enlever aParcourir de nonParcourus
        del nonParcourus[str(aParcourir.id)]

        #pour chaque voisin de aParcourir :
        voisins = getVoisins(aParcourir)
        for voisin in voisins :
            if distances[str(voisin.id)] < 0 or distances[str(voisin.id)] > distances[str(aParcourir.id)] + partie.plateau["lignes"][str(aParcourir.id)+";"+str(voisin.id)].longueur :
                distances[str(voisin.id)] = distances[str(aParcourir.id)] + partie.plateau["lignes"][str(aParcourir.id)+";"+str(voisin.id)].longueur
                precedences[str(voisin.id)] = aParcourir.id

    chemin = []
    n = vers.id
    while n != de.id :
        chemin.append(n)
        n = precedences[str(n)]
    chemin.append(de.id)

    chemin.reverse()
    distanceTotale = distances[str(vers.id)]

    return {"chemin" : chemin, "longueur" : distanceTotale}
