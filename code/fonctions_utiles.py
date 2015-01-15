def peutEnvoyer(noeud):
    
    total = noeud.off
    
    for arete in noeud.aretesConnectees:
        for mouvement in arete.mouvements:
            if (mouvement.proprio != noeud.proprio and mouvement.destination == noeud.id)
                total -= mouvement.nbUnites
    
    if (total < 0) : total = 0
    
    return total

def doitEnvoyer(partie, noeud_attaquant, noeud_defenseur):
    
    total_noeud = noeud_defenseur.off + noeud_defenseur.defensives
    total_from_us = 0
    total_from_other = 0
    a_envoyer = 0
    
    for arete in noeud_defenseur.aretesConnectees:
        for mouvement in arete.mouvements :
            
            if (mouvement.destination == noeud_defenseur.id):
                
                if (mouvement.joueur == noeud_defenseur.proprio) :
                    total_noeud += mouvement.nbUnites
                elif (mouvement.joueur == partie.me) :
                    total_from_us += mouvement.nbUnites
                else :
                    total_from_other += mouvement.nbUnites
            
            if (mouvement.destination == noeud_attaquant.id and ):
                total_noeud += mouvement.nbUnites

    #prendre en compte les mouvements sur l'arete noeuddef noeudattaquant et qui vont vers noeud attaquant
  
    a_envoyer = abs(total_noeud - total_from_other) - total_from_us        
    if (a_envoyer < 0) : a envoyer = 0
    
    return a_envoyer

def peutCapturer(partie, noeud_attaquant, noeud_defenseur):
    
    capacite_off = peutEnvoyer(noeud_attaquant)
    units_necessaires = doitEnvoyer(partie, noeud_attaquant, noeud_defenseur)
    
        
    if(capacite_off > units_necessaires):
        reponse = True
        
    else : reponse = False
    
    return reponse

