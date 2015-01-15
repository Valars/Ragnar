'''Nom : Partie

Attributs : matchid : Chaine de caractères : Identifiant de la partie
            uid     : Chaine de caractères : Identifiant du joueur pour tout le tournoi
            me      : Int                  : Identifiant du joueur dans la partie
            speed   : Int                  : Donne la vitesse du jeu (Hypothétique)
            plateau : Liste                : Contient la liste des objets Noeud ainsi que la liste des objets Arete de
                                              tout le plateau
                                              pour être précis : le plateau se décompose en deux : plateau["noeuds"] et plateau["lignes"]
                                              dans plateau["noeuds"] on a un dictionnaire contenant les noeuds, chaque noeud ayant comme clé son id
                                                ex. : plateau["noeuds"]["1"] désigne le noeud d'id 1
                                              idem pour les lignes
                                                ex. : plateau["lignes"]["1;2"] désigne l'arete ayant pour noeud1 le noeud d'id 1 et pour noeud2 le noeud d'id 2
                                                /!\ cependant, si l'arete est définie 1;2, on ne peut pas la désigner par 2;1 ! :)
'''

class Partie :
    def __init__(self, matchid="", uid="", speed=-1, me=-1, plateau=[]):
        self.matchid = matchid
        self.uid = uid
        self.speed = speed
        self.me = me
        self.plateau = plateau

    def printPartie(self) :
        print(self.uid+"@"+self.matchid)
        print("vitesse : "+str(self.speed)+" je suis le joueur "+str(self.me))

    def detailPlateau(self) :
        print("NOEUDS")
        print("##################################################")
        for idNoeud in self.plateau["noeuds"] :
            print("noeud '"+idNoeud+"' :")
            print(self.plateau["noeuds"][idNoeud])
            print("aretes connectees : ")
            for arete in self.plateau["noeuds"][idNoeud].aretesConnectees :
                print(str(arete))
                print(str(arete.noeud1.id)+"-"+str(arete.noeud2.id)+"("+str(arete.noeud1)+"-"+str(arete.noeud2)+")")
            print("##################################################")
        print("------------------------------------------------------------")
        print("ARETES")
        print("##################################################")
        for idArete in self.plateau["lignes"] :
            print("arete '"+idArete+"' :")
            print(self.plateau["lignes"][idArete])
            print(str(self.plateau["lignes"][idArete].noeud1.id)+"-"+str(self.plateau["lignes"][idArete].noeud2.id)+" ("+str(self.plateau["lignes"][idArete].noeud1)+"-"+str(self.plateau["lignes"][idArete].noeud2)+")")
            print("mouvements :")
            for mouvement in self.plateau["lignes"][idArete].mouvements :
                print(mouvement)
            print("##################################################")
