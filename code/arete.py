class Arete :
        def __init__(self, noeud1, noeud2, longueur, mouvements) :
            self.noeud1 = noeud1
            self.noeud2 = noeud2
            self.longueur = longueur
            self.mouvements = mouvements

        def printArete(self) :
            print("Arete de " + str(self.noeud1.id) + " vers "+str(self.noeud2.id))
            print("Longueur : "+str(self.longueur))
            print("#####")

        def afficher(self, canva) :
            canva.create_line(self.noeud1.x+self.noeud1.radius,self.noeud1.y+self.noeud1.radius,self.noeud2.x+self.noeud2.radius,self.noeud2.y+self.noeud2.radius)
            textx = (self.noeud1.x+self.noeud1.radius+self.noeud2.x+self.noeud2.radius)/2
            texty =(self.noeud1.y+self.noeud1.radius+self.noeud2.y+self.noeud2.radius)/2
            canva.create_text(textx,texty, text=str(self.longueur)+"ms", font=('Helvetica', 10))

            canva.pack()
