#Elkilani Narmin
import fltk

def charger(file : int) -> tuple:
    """ fonction permettant de lire et de charger des donjons prédéfinis
    et stockés dans des fichiers. """
    
    file_name = "map" + str(file)
    with open(f'{file_name}.txt','r', encoding="utf8", errors='ignore') as f:
        donjon = []
        aventurier = {}
        dragons = []
        for line in f:
                if line[0] in ["A", "D"]:
                        break
                donjon.append([])
                for i in line:
                        if len (donjon[len(donjon)-1]) > 6:
                                break
                        if i == "╬":
                                donjon[len(donjon)-1].append((True, True, True, True))
                        elif i == "╠":
                                donjon[len(donjon)-1].append((True, True, True, False))
                        elif i == "╣":
                                donjon[len(donjon)-1].append((True, False, True , True))
                        elif i == "╔":
                                donjon[len(donjon)-1].append((False, True, True , False))
                        elif i == "╗":
                                donjon[len(donjon)-1].append((False, False, True , True))
                        elif i == "╝":                         
                                donjon[len(donjon)-1].append((True, False, False, True))
                        elif i == "╚":
                                donjon[len(donjon)-1].append((True, True, False, False))                                
                        elif i == "╥":
                                donjon[len(donjon)-1].append((False, False, True, False))
                        elif i == "╨":
                                donjon[len(donjon)-1].append((True, False, False, False))
                        elif i == "╩":
                                donjon[len(donjon)-1].append((True, True, False, True))
                        elif i == "╦":
                                donjon[len(donjon)-1].append((False, True, True, True))
                        elif i == "╡": 
                                donjon[len(donjon)-1].append((False, False, False, True))
                        elif i == "╞":
                                donjon[len(donjon)-1].append((False, True, False ,False))
                        elif i == "═":
                                donjon[len(donjon)-1].append((False, True, False , True))
                        elif i == "║":
                                donjon[len(donjon)-1].append((True, False, True, False))
        # Aventurier
        f.seek(0)
        list_lines = f.readlines()
        A = list_lines[6]
        aventurier["position"] = (int(A[2]),int(A[4]))
        aventurier["niveau"] = 1
        #dragons
        f.seek(0)
        D = list_lines[7:]
        for i in D:
                dragons.append({})
                dragons[len(dragons)-1]["position"] = (int(i[2]), int(i[4]))
                dragons[len(dragons)-1]["niveau"] = int(i[6])
        return (donjon,aventurier,dragons)
    

#Gestion du donjon
def pivoter(donjon:list, position : tuple):
       """ fonction modifiant la liste de listes de salles donjon en faisant
        pivoter la salle se trouvant aux coordonnées position de 90 degrés dans le sens horaire. """
       up , right , down , left = donjon[position[0]][position[1]]    
       donjon[position[0]][position[1]] = (left, up, right, down)

def connecte (donjon:list, position1:tuple, position2:tuple) -> bool:
       """ fonction vérfiant si deux positions du donjon sont adjacentes et connectées"""
       connecte = False
       adjacent = False
       x1,y1 = position1
       x2,y2 = position2
       rg = list(range(0,6))
       if x1 not in rg or x2 not in rg or y1 not in rg or y2 not in rg :
              return False
       else:
              salle1 = donjon[x1][y1]
              salle2 = donjon[x2][y2]

       up1,right1, down1, left1 = salle1
       up2, right2, down2, left2 = salle2
       if ((x1 == x2) and (abs(y1-y2) == 1)) or ((y1 == y2)and abs(x1- x2) == 1):
              adjacent = True
       else: 
              return False
       if x1 == x2 :
                if y1 < y2 and (right1 and left2): 
                    connecte = True
                elif  y1 > y2 and (left1 and right2):
                    connecte = True
                else: 
                    return False
       if y1 == y2 :
                if x1 < x2 and (down1 and up2):
                    connecte = True
                elif  x1 > x2 and (up1 and down2):
                    connecte = True
                else: 
                    return False
       return adjacent and connecte
       
       

def connected_pos (donjon: list, position: tuple) -> list:
       """ fonction renvoyant une liste des positions connectées à une position donnée en argument"""
       connected_l = []
       x , y = position
       potential = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
       for i in potential:
              if connecte(donjon, position, i):
                     connected_l.append(i)
       return connected_l


# dragons
def dragons_pos (dragons : list) -> list:
       """ fonction retournant une liste des positions des dragons"""
       dragon_pos = []
       for ele in dragons:
              dragon_pos.append(ele["position"])
       return dragon_pos

def dragons_niv (dragons : list) -> list:
       """ fonction retournant une liste des niveaux des dragons"""
       dragon_niv = []
       for ele in dragons:
              dragon_niv.append(ele["niveau"])
       return dragon_niv

def dragons_info ( dragons : list, dragon_pos :list, dragon_niv: list) -> list:
       """ fonction renvoyant un dictionnaire dont les clés sont les positions des dragons 
       et les valeurs sont les niveaux associés
       """
       dragons_dict = {}
       for i in range(len(dragon_pos)):
              dragons_dict[dragon_pos[i]] = dragon_niv[i]
       return dragons_dict


# Intention de l'aventurier
def intention (donjon : list, position : tuple , dragons : list, dragon_pos :list, dragon_dict: dict, chemins, visite = set(), chemin = []):
        """ fonction modifiant la liste chemins pour qu'elle contient tous les chemins accessibles aux dragons"""       
        if position in dragon_pos:  
              chemin.append(position)
              chemins.append((chemin + [position], dragon_dict[position]))
              chemins[len(chemins)-1][0].pop()
              return
        chemin.append(position)
        if position in visite:
              return
        visite.add(position)
        lst = connected_pos(donjon,position)
        for n in lst:
              intention(donjon, n, dragons, dragon_pos, dragon_dict, chemins, visite, chemin)
              chemin.pop()

        return

def chemin(donjon: list, dragons: list, chemins: list) -> list:
       """fonction renvoyant le chemin au dragon de plus haut niveau au format [([chemin], niveau)] """
       niv = []
       for ele in chemins:
              niv.append(ele[len(ele)-1])
       m = max(niv)
       return chemins[niv.index(m)]



# Tour de l'aventurier
def rencontre(aventurier: dict, dragons: dict, dragon_pos: list, dragon_dict: dict) -> bool:
       """ fonction testant si l'aventurier est à la même position qu'un
            dragon, et en applique les conséquences 
            """
       if aventurier["position"] in dragon_pos:
              niveau_dragon = dragon_dict[aventurier["position"]]
              if aventurier["niveau"] >= niveau_dragon:
                     dragons.pop(niveau_dragon - 1)
                     return True
              else:
                     # aventurier tué
                     print("l'aventurier est tué!")
                     return False


def fin_partie(aventurier: dict, dragons: list)-> int:
       """ la fonction renvoie 1 si la partie est gagnée (tous les dragons
        ont été tués), -1 si la partie est perdue (l aventurier a été tué),
        et 0 si la partie continue """
       
       if len(dragons) == 0:
              return 1
       if len(aventurier) > 1:
              return -1
       else:
              return 0 
       


# partie graphique
def cree_plateau():
    """ fonction créant le plateau"""
    plateau = []
    plateau += [[("black")]*24]
    plateau += [[("black")]+22*[("white")]+[("black")] for _ in range(22)]
    plateau += [[("black")]*24]

    for j in [3,4,7,8,11,12,15,16,19,20]:
        plateau[3][j] = "black"
        plateau[4][j] = "black"
        plateau[19][j] = "black"
        plateau[20][j] = "black"

    for j in range(3, 21):
        plateau[7][j] = "black"
        plateau[8][j] = "black"

    for i in range(9, 17):
        plateau[i][11] = "black"
        plateau[i][12] = "black"
    
    for j in range(4,8):
        plateau[11][j] = "black"
    
    for j in range(3,9):
        plateau[11][j] = "black"
        plateau[12][j] = "black"

    for j in range(15, 21):
        plateau[11][j] = "black"
        plateau[12][j] = "black"

    for j in range(3,9):
        plateau[15][j] = "black"
        plateau[16][j] = "black"

    for i in range(17, 20):
        plateau[i][7] = "black"
        plateau[i][8] = "black"

    for j in range(15, 21):
        plateau[15][j] = "black"
        plateau[16][j] = "black"

    for i in range(17, 20):
        plateau[i][15] = "black"
        plateau[i][16] = "black"

    return plateau

def affiche_plateau(plateau, maj = True):
    """ fonction affichant le plateau"""

    fltk.efface_tout()
    for i in range(len(plateau)):
        for j in range(len(plateau[0])):
            couleur = plateau[i][j] 
            fltk.rectangle(j*25,i*25,(j+1)*25,(i+1)*25, remplissage = couleur)

    fltk.image(250, 50, 'media/Knight_s.png',
    largeur = 20, hauteur = 40, ancrage = 'center', tag = 'a')
    fltk.image(150, 150, 'media/Dragon_s.png',
    largeur = 30, hauteur = 40, ancrage = 'center', tag = 'd1')
    fltk.texte(160, 125, "1", couleur= "black", taille = 20, tag = "t1")
    fltk.image(50, 250, 'media/Dragon_s.png',
    largeur = 30, hauteur = 40, ancrage = 'center', tag = 'd2')
    fltk.texte(60, 225, "2", couleur= "black", taille = 20, tag = "t2")
    fltk.image(550, 250, 'media/Dragon_s.png',
    largeur = 30, hauteur = 40, ancrage = 'center', tag = 'd3')
    fltk.texte(560, 225, "3", couleur= "black", taille = 20, tag = "t3")

    if maj:
        fltk.mise_a_jour()


def coordonnee_points(position : tuple) -> tuple:
    """ fonction retournant les coordonnés du centre d'une salle à partir de sa position"""
    coordonnee = [0,0] # car on peut pas modifier les elements d'un tuple
    coordonnee[1] = 50 + ((position[0] - 0) * 100)
    coordonnee[0] = 50 + ((position[1] - 0) * 100)
    return tuple(coordonnee) 


def trace_ligne(chemins : tuple):
    """fonction tracant le chemin de l'aventurier"""
    chemin = chemins[0]
    lst_cordonnee = []
    for i in chemin:
        lst_cordonnee.append(coordonnee_points(i))
    for i in range(len(lst_cordonnee) - 1):
        fltk.ligne(lst_cordonnee[i][0], lst_cordonnee[i][1], lst_cordonnee[i+1][0], lst_cordonnee[i+1][1], couleur = 'red', epaisseur = 5)
    



def appliquer_chemin( aventurier: dict, dragons: dict, dragon_pos: list, dragon_dict: dict, chemins : tuple):
    """ fonction déplacant l’aventurier le long du chemin"""
    if rencontre(aventurier, dragons, dragon_pos, dragon_dict):
        pass
    else: 
        chemin = chemins[0]
        lst_cordonnee = []
        for i in chemin:
            lst_cordonnee.append(coordonnee_points(i))
        fltk.efface("a")
        for i in range(len(lst_cordonnee)):
            fltk.image(lst_cordonnee[i][0],lst_cordonnee[i][1], 'media/Knight_s.png',
            largeur = 20, hauteur = 40, ancrage = 'center', tag = 'a')
            aventurier["position"] = chemin[i]
            if i != len(lst_cordonnee) - 1:
                fltk.efface("a")
                fltk.mise_a_jour()
            else:
                aventurier["position"] = chemin[i]
                niveau_dragon = dragon_dict[aventurier["position"]]
                if rencontre(aventurier, dragons, dragon_pos, dragon_dict):
                                      tag = "d" + str(niveau_dragon)
                                      fltk.efface(tag)
                else:
                      fltk.efface("a")
                      fltk.texte(300, 350, "tour perdu", police = "Courier", taille = 40, couleur="red", ancrage='center')
                      

       


# execution du code
#l'utilisateur choisit la map à jouer et on vérifie qu'il saisit
# un nombre dans [1,2,3,4,5]
if __name__ == '__main__':
      
      
      fltk.cree_fenetre(600, 600)
      plateau = cree_plateau()
      affiche_plateau(plateau)
      print("Bienvenue au jeu")
    # fonctionnalite pour choisir la map, ici le plateau est fait seulement pour la map5
    #   map_numbers = [1,2,3,4,5]
    #   file_number = None
    #   while file_number not in map_numbers:
    #     try:
    #         file_number = int(input("Chosissez le nombre du map : 1 ou 2 ou 3 ou 4 ou 5 "))
    #     except ValueError:
    #         print("S'il vous plait entrez un nombre ") 
      donjon, aventurier, dragons = charger(5)
      dragon_pos = dragons_pos(dragons)
      dragon_niv = dragons_niv(dragons)
      dragon_dict = dragons_info(dragons, dragon_pos, dragon_niv)
      chemins_1 = []
      intention(donjon, aventurier["position"], dragons, dragon_pos, dragon_dict, chemins_1, visite = set(), chemin = [] )
      chemins = chemin(donjon , dragons , chemins_1)
      while True:
             ev = fltk.donne_ev()
             tev = fltk.type_ev(ev)
             if tev == "Touche":
                trace_ligne(chemins)
                appliquer_chemin(aventurier, dragons, dragon_pos, dragon_dict, chemins)
             fltk.mise_a_jour()

      fltk.ferme_fenetre()
