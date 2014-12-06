class Arete :
        def __init__(self, noeud1, noeud2, longueur, mouvements) :
            self.de = noeud1
            self.vers = noeud2
            self.longueur = longueur
            self.mouvements = mouvements

        def printArete(self) :
            print("Arete de " + str(self.noeud1) + " vers "+str(self.noeud2))
            print("Longueur : "+str(self.longueur))
            print("#####")

        def afficher(self, x,y,x1,y1,canva) :
            canva.create_line(x,y,x1,y1)
            textx = (x+x1)/2
            texty =(y+y1)/2
            canva.create_text(textx,texty, text=str(self.longueur)+"ms", font=('Helvetica', 10))
            
            canva.pack()
