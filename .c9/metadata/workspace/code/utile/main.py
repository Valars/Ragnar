{"filter":false,"title":"main.py","tooltip":"/code/utile/main.py","undoManager":{"mark":0,"position":0,"stack":[[{"group":"doc","deltas":[{"start":{"row":4,"column":0},"end":{"row":8,"column":41},"action":"remove","lines":["","import re","","window = Tk()","w = Canvas(window, width=400, height=400)"]},{"start":{"row":4,"column":0},"end":{"row":4,"column":21},"action":"insert","lines":["from parsers import *"]},{"start":{"row":11,"column":0},"end":{"row":47,"column":132},"action":"remove","lines":["'''prend une chaine en paramètre de la forme suivante :","INIT<matchid>TO<#players>[<me>];<speed>;\\","       <#cells>CELLS:<cellid>(<x>,<y>)'<radius>'<offsize>'<defsize>'<prod>,...;\\","       <#lines>LINES:<cellid>@<dist>OF<cellid>,...","","       <me> et <owner> désignent des numéros de 'couleur' attribués aux joueurs. La couleur 0 est le neutre.","       le neutre n'est pas compté dans l'effectif de joueurs (<#players>).","       '...' signifie que l'on répète la séquence précédente autant de fois qu'il y a de cellules (ou d'arêtes).","       0CELLS ou 0LINES sont des cas particuliers sans suffixe.","       <dist> est la distance qui sépare 2 cellules, exprimée en... millisecondes !","       /!\\ attention: un match à vitesse x2 réduit de moitié le temps effectif de trajet d'une cellule à l'autre par rapport à l'indication <dist>.","       De manière générale temps_de_trajet=<dist>/vitesse (division entière).","","INIT 20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2]; 1 ; 3CELLS: 1(23,9) ' 2 ' 30 ' 8 ' I ,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I ; 2LINES:1@3433OF2,1@6502OF3","","et retourne le matchid, la vitesse du jeu, et la liste des noeuds et des aretes du plateau sous forme de liste d'objets","","'''","def initPlateau(chaine) :","    noeuds = []","    lignes = []","","    touteslesinfos = re.findall(\"INIT(.+)TO[0-9]+\\[([0-9]+)\\];([0-9]+);[0-9]+CELLS:(.+);[0-9]+LINES:(.+)\",chaine)","    touteslesinfos = touteslesinfos[0]","","    cells = re.findall(\"([0-9]+\\([0-9]+,[0-9]+\\)'[0-9]+'[0-9]+'[0-9]+'[I]+)\",touteslesinfos[3])","    for cell in cells :","        infos = re.findall(\"([0-9]+)\\(([0-9]+),([0-9]+)\\)'([0-9]+)'([0-9]+)'([0-9]+)'([I]+)\",cell)","        noeuds.append(Noeud(int(infos[0][0]), int(infos[0][1]), int(infos[0][2]), int(infos[0][3]), int(infos[0][4]), int(infos[0][5]), infos[0][6]))","","    lines = re.findall('[0-9]+@[0-9]+OF[0-9]+',touteslesinfos[4])","","    for line in lines :","        infoLigne = re.findall('([0-9]+)@([0-9]+)OF([0-9]+)', line)","        lignes.append(Arete(int(infoLigne[0][0]), int(infoLigne[0][2]), int(infoLigne[0][1])))","","    return {\"matchid\":touteslesinfos[0], \"speed\":int(touteslesinfos[2]),\"noeuds\":noeuds,\"lignes\":lignes,\"me\":int(touteslesinfos[1])}"]},{"start":{"row":11,"column":0},"end":{"row":12,"column":0},"action":"insert","lines":["",""]},{"start":{"row":25,"column":25},"end":{"row":25,"column":26},"action":"remove","lines":["1"]},{"start":{"row":25,"column":25},"end":{"row":25,"column":33},"action":"insert","lines":["\"lignes\""]},{"start":{"row":26,"column":18},"end":{"row":27,"column":44},"action":"remove","lines":["plateau[0][ligne.de-1]","        noeudVers = plateau[0][ligne.vers-1]"]},{"start":{"row":26,"column":18},"end":{"row":27,"column":32},"action":"insert","lines":["ligne.noeud1","        noeudVers = ligne.noeud2"]},{"start":{"row":33,"column":25},"end":{"row":33,"column":26},"action":"remove","lines":["0"]},{"start":{"row":33,"column":25},"end":{"row":33,"column":33},"action":"insert","lines":["\"noeuds\""]},{"start":{"row":44,"column":0},"end":{"row":80,"column":0},"action":"remove","lines":["'''","    STATE<matchid>IS<#players>;<#cells>CELLS:<cellid>[<owner>]<offunits>'<defunits>,...;\\","    <#moves>MOVES:<cellid><direction><#units>[<owner>]@<timestamp>'...<cellid>,...","","","\"STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3\"","","<timestamp> en millisecondes, donnée à vitesse x1 : top départ des unités de la cellule source.","<direction> désigne le caractère '>' ou '<' et indique le sens des unités en mouvement en suivant la pointe de flèche.","'''","'''","    prend une chaine Etat telle que retournée par le serveur de l'appel à etat()","    et retourne une liste : des cellules (id,owner,atk,def) et des mouvements (celluleIDFrom,direction[<>],nbUnits,owner,timestamp d'envoi des unités)","'''","def parseEtat(chaine) :","    cells = re.findall(\"([0-9]+)\\[([0-9]+)\\]([0-9]+)'([0-9]+)\", chaine)","    moves = re.findall(\"MOVES:(.*)\", chaine)","    moves = moves[0].split(',')","","    noeuds = []","    mouvements = []","    for cell in cells :","        noeuds.append({\"id\":int(cell[0]),\"owner\":int(cell[1]),\"atk\":int(cell[2]),\"def\":int(cell[3])})","","    for move in moves :","        arcFrom = re.findall('^([0-9]+)', move)","        arcTo = re.findall(\"'([0-9]+)$\", move)","        arcFrom = int(arcFrom[0])","        arcTo = int(arcTo[0])","        movesSurLarc = re.findall(\"([<>])([0-9]+)\\[([0-9]+)\\]@([0-9]+)\", move)","        for lemove in movesSurLarc :","            mouvements.append({\"from\":arcFrom, \"to\":arcTo, \"direction\":lemove[0], \"nbUnits\":int(lemove[1]), \"timestamp\":int(lemove[3]), \"joueur\":int(lemove[2])})","","    return {\"noeuds\":noeuds, \"moves\":mouvements}","","",""]},{"start":{"row":45,"column":0},"end":{"row":45,"column":21},"action":"remove","lines":["plateau = initPlateau"]},{"start":{"row":45,"column":0},"end":{"row":46,"column":18},"action":"insert","lines":["global partie","partie = parseInit"]},{"start":{"row":50,"column":12},"end":{"row":50,"column":13},"action":"remove","lines":["E"]},{"start":{"row":50,"column":12},"end":{"row":50,"column":13},"action":"insert","lines":["S"]},{"start":{"row":50,"column":16},"end":{"row":50,"column":17},"action":"insert","lines":["e"]},{"start":{"row":53,"column":18},"end":{"row":53,"column":25},"action":"insert","lines":["artie.p"]},{"start":{"row":56,"column":60},"end":{"row":56,"column":72},"action":"remove","lines":["lateau[\"me\"]"]},{"start":{"row":56,"column":60},"end":{"row":56,"column":68},"action":"insert","lines":["artie.me"]},{"start":{"row":57,"column":0},"end":{"row":58,"column":0},"action":"insert","lines":["",""]},{"start":{"row":67,"column":0},"end":{"row":74,"column":68},"action":"remove","lines":["'''","    à la disposition : matchid, me, speed, plateau[2] (noeuds) plateau[3] (arêtes)","'''","","","","#affichage graphique du plateau","initGraphique(w,[plateau[\"noeuds\"],plateau[\"lignes\"]], etat[\"moves\"]"]},{"start":{"row":67,"column":0},"end":{"row":76,"column":21},"action":"insert","lines":["","","","#affichage graphique du plateau","'''window = Tk()","w = Canvas(window, width=400, height=400)","initGraphique(w,partie.plateau, etat[\"moves\"])'''","","for noeud in partie.plateau[\"noeuds\"] :","    noeud.printNoeud("]}]}]]},"ace":{"folds":[],"scrolltop":645,"scrollleft":0,"selection":{"start":{"row":44,"column":0},"end":{"row":44,"column":0},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1417873263284,"hash":"6c7506853ea0c435c1decc80eb40560e4d9ccd7a"}