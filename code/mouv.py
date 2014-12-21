from poooc import order, state, state_on_update, etime
#[0947e717-02a1-4d83-9470-a941b6e8ed07]MOV33FROM1TO4

''' Nom : mouv(laPartie, expediteur, cible, units)

    Role : Envoi d'un ordre de mouvement
    Description : Concatène les informations nécessaire en une chaine de caractères et appel la fonction order avec cette même chaine

    E : laPartie   : Partie : Informations de bases sur la partie en cours
        expediteur : Noeud  : Noeud envoyant les unités
        cible      : Noeud  : Noeud destinataire des unités
        units      : Int    : Pourcentage des unités de l'expediteur qui seront envoyés
'''

def mouv(partie, expediteur, cible, units):


    order("["+str(partie.uid)+"]MOV"+str(units)+"FROM"+str(expediteur.id)+"TO"+str(cible.id))
