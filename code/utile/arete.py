class Arete :
        def __init__(self, de, vers, longueur) :
            self.de = de
            self.vers = vers
            self.longueur = longueur

        def printArete(self) :
            print("Arete de " + str(self.de) + " vers "+str(self.vers))
            print("Longueur : "+str(self.longueur))
            print("#####")

        def afficher(self, x,y,x1,y1,canva) :
            canva.create_line(x,y,x1,y1)
            textx = (x+x1)/2
            texty =(y+y1)/2
            canva.create_text(textx,texty, text=str(self.longueur)+"ms", font=('Helvetica', 10))
            
            canva.pack()
