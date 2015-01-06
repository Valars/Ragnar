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
    '''
    if de == vers :
        return {"chemin" : [de,vers], "longueur" : 0}
    if str(de.id) not in partie.plateau["noeuds"].keys() or str(vers.id) not in partie.plateau["noeuds"].keys() :
        print(str(de.id)+";"+str(vers.id))
        return -1

    distances = {}
    order = {}

    for noeud in partie.plateau["noeuds"] :
        if noeud == str(de.id) :
            distances[noeud] = 0
        else :
            distances[noeud] = float("inf")

    nonParcourus = dict(distances)

    while len(nonParcourus) > 0 :
        mini = min(nonParcourus, key=nonParcourus.get)
        for voisin in getVoisins(getNoeud(partie,int(mini))) :
            #print("###")
            #print(str(distances[str(voisin.id)])+" > "+str(distances[mini])+"+"+str(partie.plateau["lignes"][mini+";"+str(voisin.id)].longueur))
            #print("###")
            if distances[str(voisin.id)] > distances[mini] + partie.plateau["lignes"][mini+";"+str(voisin.id)].longueur :
                distances[str(voisin.id)] = distances[mini] + partie.plateau["lignes"][mini+";"+str(voisin.id)].longueur
                nonParcourus[str(voisin.id)] = distances[mini] + partie.plateau["lignes"][mini+";"+str(voisin.id)].longueur
                print("ajout dans order de : order["+str(voisin.id)+"]="+mini)
                order[str(voisin.id)] = mini
        del nonParcourus[mini]
    return order'''











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

    while len(nonParcourus) != 0:
        #récupérer le noeud ayant la distance la plus petite positive
        distMin = distances[max(distances, key=distances.get)]
        aParcourir = getNoeud(partie,int(max(distances, key=distances.get)))

        for cle in distances :
            if distances[cle] >= 0 and distMin > distances[cle] :
                distMin = distances[cle]
                aParcourir = getNoeud(partie, int(cle))


        #enlever aParcourir de nonParcourus

        del nonParcourus[str(aParcourir.id)]

        #print("##################################")
        #print(nonParcourus)
        #print("on voulait enlever : "+str(aParcourir.id))

        #pour chaque voisin de aParcourir :
        voisins = getVoisins(aParcourir)
        for voisin in voisins :
            if distances[str(voisin.id)] == -1 or distances[str(voisin.id)] > distances[str(aParcourir.id)] + partie.plateau["lignes"][str(aParcourir.id)+";"+str(voisin.id)].longueur :
                distances[str(voisin.id)] = distances[str(aParcourir.id)] + partie.plateau["lignes"][str(aParcourir.id)+";"+str(voisin.id)].longueur
                precedences[str(voisin.id)] = aParcourir.id
        #print(str(i)+" - a parcourir : "+str(aParcourir.id))

    chemin = []
    n = vers.id
    while n != de.id :
        chemin.append(n)
        n = precedences[str(n)]
    chemin.append(de.id)

    chemin.reverse()
    distanceTotale = distances[str(vers.id)]

    return {"chemin" : chemin, "longueur" : distanceTotale}

'''
    Nom : calc_distance() (partie, noeud)

    E : partie : Partie : L'objet partie, qui contient le plateau de jeu
        noeud     : Noeud  : Noeud pour lequel on veut déterminer le plus court chemin vers les autres noeuds

'''
def calc_distances(partie):
    #print(dijkstra(partie, partie.plateau["noeuds"]["6"], partie.plateau["noeuds"]["5"]))
    print(dijkstra(partie, partie.plateau["noeuds"]["6"], partie.plateau["noeuds"]["3"]))
    time.sleep(10)
    '''for i in range(7) :
        for j in range(7) :
            if(i != j) :
                print(str(i)+" - "+str(j))
                print(dijkstra(partie, partie.plateau["noeuds"][str(i)], partie.plateau["noeuds"][str(j)]))'''
    '''for noeud_debut in partie.plateau["noeuds"]:
        for noeud_fin in partie.plateau["noeuds"]:
            if(noeud_debut != noeud_fin):
                #print("#############################################################")
                #print("distance de "+noeud_debut+" vers "+noeud_fin)
                #print(dijkstra(partie, partie.plateau["noeuds"][noeud_debut], partie.plateau["noeuds"][noeud_fin]))
                plus_court_chem = dijkstra(partie, getNoeud(partie,noeud_debut), getNoeud(partie,noeud_fin))
                partie.plateau["noeuds"][noeud_debut].distances[str(partie.plateau["noeuds"][noeud_fin].id)]= [plus_court_chem['chemin'], plus_court_chem['longueur']]
                '''
