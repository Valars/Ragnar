def getArete(partie, idNoeud1, idNoeud2):
    return partie.plateau["lignes"][str(idNoeud1)+";"+str(idNoeud2)]
    
def getNoeud(partie, id) :
    return partie.plateau["noeuds"][str(id)]