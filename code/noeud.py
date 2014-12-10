class Noeud :
    def __init__(self, id, x, y, radius, offsize, defsize, prod, proprio=-1,off=0,defenses=0,aretesConnectees=[]) :
        self.id = id
        self.proprio = proprio
        self.x = x
        self.y = y
        self.radius = radius
        self.offsize = offsize
        self.defsize = defsize
        self.prod = prod
        self.off = off
        self.defenses = defenses
        self.aretesConnectees = aretesConnectees

    def printNoeud(self) :
        print("Noeud "+str(self.id))
        print("proprio : "+str(self.proprio))
        print("coords : "+str(self.x)+";"+str(self.y))
        print("radius : "+str(self.radius))
        print("unités : "+str(self.off)+"/"+str(self.offsize) + " + "+str(self.defenses)+"/"+str(self.defsize))
        print("Production  :"+str(self.prod))
        print("Noeuds connectes : ",end='')
        for arete in self.aretesConnectees :
            print(';',end='')
            if arete.noeud1 == self :
                print(arete.noeud2.id,end='')
            else :
                print(arete.noeud1.id,end='')
        print()
        print("#####")

    def afficher(self, canva) :
        if self.proprio == 0 :
            couleur = 'white'
        elif self.proprio == 1 :
            couleur = 'blue'
        elif self.proprio == -1 :
            couleur = 'red'

        coefRadius = 20#le rayon d'un noeud = 20 * son radius
        fontSize = 5*self.radius

        centrex = self.x + self.radius * coefRadius
        centrey = self.y + self.radius * coefRadius
        canva.create_oval(self.x,self.y,self.x+self.radius*2*coefRadius,self.y+self.radius*2*coefRadius, fill=couleur, outline='black', width=1)#radius * 2 pour le diametre, *20 arbitrairement pour pouvoir avoir de la place dedans

        canva.create_text(centrex,centrey-self.radius*5,text=self.id,font=('Helvetica', fontSize))
        canva.create_text(centrex,centrey,text='atk : ' + str(self.off)+"/"+str(self.offsize), font=('Helvetica', fontSize))
        canva.create_text(centrex,centrey+self.radius*5,text='def : '+str(self.defenses)+"/"+str(self.defsize), font=('Helvetica', fontSize))
        canva.create_text(centrex,centrey+self.radius*5*2, text=self.prod, font=('Helvetica', fontSize))

        canva.pack()
