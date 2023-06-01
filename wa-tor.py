import pylab
from doctest import testmod
from random import random,randint

### CONSTANTES
# dimensions de la mer
NB_LIGNES, NB_COLONNES = 25, 25

DUREE_GESTATION_THON = 2# nombre maximal d'itérations avant la naissance éventuelle d'un thon
DUREE_GESTATION_REQUIN = 6# nombre maximal d'itérations avant la naissance éventuelle d'un requin
ENERGIE_MAX_REQUIN = 3# nombre maximal d'itérations sans manger pour un requin

# codes attribués à un nouveau poisson, pour éviter des calculs
# et faciliter la lecture du programme
CODE_REQUIN_NOUVEAU = ENERGIE_MAX_REQUIN*100+DUREE_GESTATION_REQUIN
CODE_THON_NOUVEAU = DUREE_GESTATION_THON


### VARIABLES GLOBALES
# ces deux variables globales éviteront de devoir recompter à chaque itération le nombre
# de poissons dans toute la mer
nb_thons, nb_requins = 0, 0

# cette variable sera complétée au fur et à mesure pour enregistrer l'état de la mer
etats = list()



def creer_mer_vide(lignes,cols):
    '''
    création d'une grille vide
    params: lignes est le nombres de lignes, cols est le nombre de colonnes
    return: une liste de listes contenant des zéros
    >>> creer_mer_vide(2,2)
    [[0, 0], [0, 0]]
    '''
    return [[0 for i in range(lignes)] for j in range(cols)]


def generer(proba):
    '''
    choisit entre 0 et 1 suivant une certaine probabilité
    params: proba est la probabilité désirée
    return: 0 ou 1
    >> generer(0.7)
    1
    >> generer(0.7)
    0
    '''
    if random() < proba:
        return 1
    else:
        return 0

def peupler_mer(mer,p,q):
    '''
    place dans une grille vide à deux dimensions environ p % de thons
    et q % de requins
    params: mer est une liste de listes
            p et q sont des pourcentages
    return: NoneType
    effet de bord : modifie la grille fournie en paramètre
    exemple : peupler_mer(mer,70,10) pour avoir environ 70 % de thons et 10 % de requins
    '''
    global nb_thons, nb_requins
    # conversion des pourcentages en probabilités    
    p = p / 100
    q = q / 100
    q = q / (1 - p)# pour tenir compte des cases déjà prises
    for i in range(NB_LIGNES):
        for j in range(NB_COLONNES):
            # on commence par placer des thons
            if generer(p) != 0 :# si un thon a été généré
                mer[i][j] = CODE_THON_NOUVEAU
                nb_thons += 1
            else:# la case est encore vide donc on y génére éventuellement un requin
                if generer(q) != 0 :# si un requin a été généré
                    mer[i][j] = CODE_REQUIN_NOUVEAU
                    nb_requins += 1


def choisir_case():
    '''
    choisit une case au hasard, entre (0,0) et (NB_LIGNES-1,NB_COLONNES-1)
    return : un couple d'entiers, désignant les coordonnées de la case choisie
    >> choisir_case()
    (32,87)
    '''
    return (randint(0,NB_LIGNES-1),randint(0,NB_COLONNES-1))


def voir_genre(mer, x, y):
    '''
    affiche le genre de poisson présent dans la case (x,y) de la grille mer
    params: mer est une liste de listes
            x et y sont des entiers, désignant les coordonnées de la case actuelle
    return:
    0 pour une case vide
    1 pour un thon
    2 pour un requin
    >>> ma_mer = [[312, 18, 5345], [23, 0, 0], [100, 999, 1]]
    >>> voir_genre(ma_mer,0,0)
    2
    >>> voir_genre(ma_mer,1,0)
    1
    >>> voir_genre(ma_mer,1,2)
    0
    '''
    val = mer[x][y]
    if val == 0:
        return 0# eau
    elif val<100:
        return 1# thon
    else:
        return 2# requin



def voir_temps_naissance(mer, x, y):
    '''
    affiche le temps restant avant une naissance potentielle pour un poisson situé
    dans la case (x,y) de la grille mer
    
    params: mer est une liste de listes
            x et y sont des entiers, désignant les coordonnées de la case actuelle
    return: un nombre inférieur à 100
    
    >>> ma_mer = [[312, 18, 5345], [23, 0, 0], [100, 999, 1]]
    >>> voir_temps_naissance(ma_mer,0,0)
    12
    >>> voir_temps_naissance(ma_mer,1,0)
    23
    >>> voir_temps_naissance(ma_mer,1,2)
    0
    '''
    val = mer[x][y]
    if val > 100:# requin
        return val-(val//100)*100
    elif val>0:# pas requin mais non nul donc thon
        return val
    else:# vide
        return 0


def voir_energie_requin(mer, x, y):# appelée seulement pour un requin
    '''
    affiche l'énergie d'un requin situé dans la case (x,y) de la grille mer
    params: mer est une liste de listes
            x et y sont des entiers, désignant les coordonnées de la case actuelle
    return: un entier désignant l'énergie du requin
    >>> ma_mer = [[312, 18, 5345], [23, 0, 0], [100, 999, 1]]
    >>> voir_energie_requin(ma_mer,0,0)
    3
    >>> voir_energie_requin(ma_mer,0,2)
    53
    '''
    return mer[x][y] // 100# nombre de centaines




def choisir_deplacement():
    '''
    choisit aléatoirement un déplacement parmi les quatre possibles :
    (1,0) ou (0,1) ou (-1,0) ou (0,-1)
    return: un couple de valeurs
    '''
    direc = randint(0,1)# horizontal ou vertical
    signe = 2*randint(0,1)-1# ce qui donne -1 ou 1
    if direc == 0:
        return (signe,0)
    else:
        return (0,signe)



def calculer_nouvelle_case(x,y):
    '''
    calcule les coordonnées d'une case en gérant le cas où x>NB_LIGNES et y>NB_COLONNES
    return: un couple de valeurs désignant les coordonnées rectifiées
    '''
    return (x % NB_LIGNES,y % NB_COLONNES)



def choisir_case_autour(x,y,depl):
    '''
    choisit un mouvement parmi ceux présents dans la liste depl
    puis calcule les coordonnées du point d'arrivée
    params: x et y sont des entiers, désignant les coordonnées de la case actuelle
            depl est une liste de déplacements possibles
    return: un t-uple contenant les coordonnées de la case choisie
            et le numéro de déplacement choisi
    
    >> NB\_LIGNES,NB\_COLONNES = 3,3 # ici x et y ne peuvent aller que de 0 à 2
    >> deplacements = [(-1,0),(0,1),(0,-1)]
    >> choisir_case_autour(0,1,deplacements)
    (2,1,0)
    >> choisir_case_autour(0,1,deplacements)
    (0,2,1)
    >> choisir_case_autour(0,1,deplacements)
    (0,0,2)
    '''
    k = randint(0,len(depl)-1)
    (u,v) = depl[k]
    (x_fin,y_fin) = calculer_nouvelle_case(x+u,y+v)
    return (x_fin,y_fin,k)



def chercher_autour(mer,x,y,but):
    '''
    chercher dans les quatre cases voisines s'il y a une case vide ou un thon
    params:
    mer : une liste de listes représentant la mer
    x et y sont des entiers, désignant les coordonnées de la case actuelle
    but : 0 pour une case vide ou 1 pour un thon
    return: les coordonnées de la case contenant le but cherché
            ou (-1,-1) si le but n'a pas été trouvé
    
    >> NB_LIGNES=3
    >> NB_COLONNES=3
    >> ma_mer=[[1,0,1],[1,1,1],[1,1,1]]
    >> chercher_autour(ma_mer,0,0,0) # recherche d'une case vide autour de la case (0,0)
    (0,1)
    >> chercher_autour(ma_mer,0,0,1) # recherche d'un thon autour de la case (0,0)
    (0,2)
    >> chercher_autour(ma_mer,0,0,1) # recherche d'un thon autour de la case (0,0)
    (2,0)
    >> chercher_autour(ma_mer,0,0,1) # recherche d'un thon autour de la case (0,0)
    (1,0)
    '''
    deplacements = [(1,0),(-1,0),(0,1),(0,-1)]
    i = 0
    trouve = False
    while (i<4) and (trouve == False):
        # choix d'un déplacement au hasard et nouvelles coordonnées
        (x_fin,y_fin,k) = choisir_case_autour(x,y,deplacements)
        if voir_genre(mer,x_fin,y_fin) == but:
            trouve = True
        else:
            i+=1
            del deplacements[k]# on supprime le déplacement testé
    if i == 4:# le but (case vide ou thon) n'a pas été trouvé
        return (-1,-1)
    else:
        return (x_fin,y_fin)



def comportement_thon(mer,x,y):# appelée seulement pour un thon
    global nb_thons # il peut y avoir une naissance
    '''
    déplace un thon présent dans la case (x,y) et donne naissance à un nouveau thon si
    nécessaire
    params:   mer : une liste de listes représentant la mer
              x et y sont des entiers, désignant les coordonnées de la case actuelle
    return: NoneType
    effet de bord : modifie la grille fournie en paramètre
    
    
    >>> NB_LIGNES=3
    >>> NB_COLONNES=3
    >>> DUREE_GESTATION_THON = 2
    >>> ma_mer=[[2,0,2],[131,231,1],[411,1,1]]
    >>> comportement_thon(ma_mer,0,0)# pour agir sur le thon présent en (0,0)
    >>> ma_mer
    [[0, 1, 2], [131, 231, 1], [411, 1, 1]]
    >>> comportement_thon(ma_mer,0,1)# pour agir sur le thon présent en (0,1)
    >>> ma_mer
    [[2, 2, 2], [131, 231, 1], [411, 1, 1]]
    >>> comportement_thon(ma_mer,2,1)# pour agir sur le thon présent en (2,1)
    >>> ma_mer
    [[2, 2, 2], [131, 231, 1], [411, 2, 1]]
    '''
    (x_fin,y_fin) = chercher_autour(mer,x,y,0)# le thon cherche une case vide autour
    
    tps = voir_temps_naissance(mer, x, y) - 1# diminution du temps avant la prochaine naissance
    
    if x_fin != -1:# une case vide trouvée
        if tps == 0:# naissance d'un thon
            nb_thons += 1
            mer[x_fin][y_fin] = CODE_THON_NOUVEAU    # on déplace le thon et on le remet 
                                                     # à neuf
        else:
            mer[x_fin][y_fin] = mer[x][y]-1# on déplace le thon en diminuant son temps de gestation
            mer[x][y] = 0
    
    if tps == 0:
        mer[x][y] = CODE_THON_NOUVEAU # naissance d'un nouveau thon ou remise au max
                                      # du thon initial s'il ne s'est pas déplacé





def deplacer_sans_engendrer_requin(mer,x,y,x_fin,y_fin,en,tps):
    '''
    déplace un requin présent dans la case (x,y) vers la case (x_fin,y_fin)
    params:   mer : une liste de listes représentant la mer
              x et y sont des entiers, désignant les coordonnées de la case de départ
              x_fin et y_fin sont des entiers, désignant les coordonnées de la case d'arrivée
              en est un entier désignant l'énergie actuelle du requin
              tps est un entier désignant le temps restant une prochaine naissance
    return: NoneType
    effet de bord : modifie la liste fournie en paramètre
    >>> ma_mer=[[2,0,2],[131,231,1],[411,1,1]]
    >>> deplacer_sans_engendrer_requin(ma_mer,2,0,2,1,3,10) # déplacement du requin présent en (2,0) vers (2,1), son énergie après réduction est 3 et son temps av. naiss. 10
    >>> ma_mer
    [[2, 0, 2], [131, 231, 1], [0, 310, 1]]
    '''
    mer[x_fin][y_fin] = en*100+tps # on déplace le requin en calculant son code
    mer[x][y] = 0


def deplacer_et_engendrer_requin(mer,x,y,x_fin,y_fin,en):
    '''
    déplace un requin présent dans la case (x,y) vers la case (x_fin,y_fin)
    et donne naissance à un nouveau requin dans la case (x,y)
    remet également au max. le temps de gestation du requin adulte
    params:   mer : une liste de listes représentant la mer
              x et y sont des entiers, désignant les coordonnées de la case de départ
              x_fin et y_fin sont des entiers, désignant les coordonnées de la case d'arrivée
              en est un entier désignant l'énergie actuelle du requin
    return: NoneType
    effet de bord : modifie la grille fournie en paramètre
    >>> DUREE_GESTATION_REQUIN = 6
    >>> ENERGIE_MAX_REQUIN = 3
    >>> CODE_REQUIN_NOUVEAU = 306
    >>> ma_mer=[[2,0,2],[131,201,1],[411,1,1]]
    >>> deplacer_et_engendrer_requin(ma_mer,1,1,2,1,1)# déplacement du requin présent en (1,1) vers (2,1), son énergie après réduction est 1 (et son temps av. naiss. est remis au max)
    >>> ma_mer
    [[2, 0, 2], [131, 306, 1], [411, 106, 1]]
    '''
    global nb_requins
    nb_requins += 1
    mer[x][y] = CODE_REQUIN_NOUVEAU # naissance d'un nouveau requin en (x,y)
    mer[x_fin][y_fin] = en*100+DUREE_GESTATION_REQUIN # on déplace le requin et on remet 
                                                    # au max son temps de gestation






def comportement_requin(mer,x,y):
    '''
    déplace un requin présent dans la case (x,y) vers un thon ou vers une case vide
    ou le laisse à sa place au pire et donne naissance à un nouveau requin si nécessaire
    params:   mer : une liste de listes représentant la mer
              x et y sont des entiers, désignant les coordonnées de la case actuelle
    return: NoneType
    effet de bord : modifie la liste fournie en paramètre
    
    >> NB_LIGNES=3
    >> NB_COLONNES=3
    >> ma_mer=[[5,0,21],[131,231,1],[411,1,1]]
    >> deplacer_requin(ma_mer,1,0)
    >> ma_mer
    [[530, 0, 21], [0, 231, 1], [411, 1, 1]]
    ou
    [[5, 0, 21], [0, 231, 530], [411, 1, 1]]
    '''
    global nb_thons, nb_requins

    (x_fin,y_fin) = chercher_autour(mer,x,y,1)# le requin cherche un thon
    
    tps = voir_temps_naissance(mer, x, y) - 1# diminution du temps avant la prochaine naissance
    if x_fin != -1:#un thon trouvé
        nb_thons -= 1
        if tps == 0:# naissance d'un requin et remise au max de l'énergie
            deplacer_et_engendrer_requin(mer,x,y,x_fin,y_fin,ENERGIE_MAX_REQUIN)
        else:# pas de naissance
            # on déplace le requin en diminuant
            # son temps de gestation mais en remettant son énergie au max
            deplacer_sans_engendrer_requin(mer,x,y,x_fin,y_fin,ENERGIE_MAX_REQUIN,tps)
    else:# pas de thon en vue
        # la question de la survie se pose
        en = voir_energie_requin(mer,x,y) - 1
        if en == 0:# mort
            mer[x][y] = 0
            nb_requins -= 1
        else:
            (x_fin,y_fin) = chercher_autour(mer,x,y,0)# on cherche une case vide
            if x_fin != -1:#une case vide trouvée
                if tps == 0:# naissance d'un requin
                    deplacer_et_engendrer_requin(mer,x,y,x_fin,y_fin,en)
                else:# simple déplacement sans naissance
                    deplacer_sans_engendrer_requin(mer,x,y,x_fin,y_fin,en,tps)
            else:# le requin n'est pas mort mais ne peut se déplacer
                mer[x][y] = mer[x][y]-101  # on diminue son temps
                                           # de gestation et son énergie
            

def afficher_mer_textuel(mer,nb_iter):
    '''
    affiche la grille mer dans la console en symbolisant :
    '_' pour de l'eau ; 'R' pour un requin ; 'T' pour thon
    params:     mer : une liste de listes représentant la mer
                nb_iter : le nombre d'itérations effectuées
    return: NoneType
    >>> ma_mer=[[5,0,21],[131,231,1],[411,1,1]]
    >>> afficher_mer_textuel(ma_mer,500)
    Après 500 étapes :
    T _ T 
    R R T 
    R T T 
    '''
    print('Après',nb_iter,'étapes :')
    for ligne in mer:
        for val in ligne:
            if val == 0:
                print('_',end=' ')
            elif val>100:
                print('R',end=' ')
            else:
                print('T',end=' ')
        print()


def afficher_mer_visuel(mer,nb_iter):
    '''
    affiche la grille mer dans une fenêtre graphique en symbolisant :
    un point rouge pour un requin ; un point bleu pour un thon
    params:     mer : une liste de listes représentant la mer
                nb_iter : le nombre d'itérations effectuées
    return: NoneType
    '''
    couleurs = ['w','b','r']
    styles = ['o','8','4']
    pylab.axis([-1, NB_LIGNES, -1, NB_COLONNES])
    pylab.xlabel('',fontsize=0)
    pylab.ylabel('',fontsize=0)
    titre = 'Etat de la mer après '+str(nb_iter)+' itérations'
    pylab.title(titre)
    for i in range(NB_LIGNES):
        for j in range(NB_COLONNES):
            k = voir_genre(mer,i,j)
            coul = couleurs[k]
            mark = styles[k]
            if k==2 or k==0:
                pylab.scatter(j, NB_LIGNES-1-i,s = 120, c='w')# pour l'esthétique...
            pylab.scatter(j, NB_LIGNES-1-i,s = 100, c=coul, marker=mark)
            pylab.pause(0.00000000000000001)# sans cela, pas d'affichage...
    



import pygame
from pygame.locals import *


def afficher_mer_pygame(mer,nb_iter):
    '''
    affiche la grille mer dans une fenêtre graphique en symbolisant :
    un point rouge pour un requin ; un point bleu pour un thon
    params:     mer : une liste de listes représentant la mer
                nb_iter : le nombre d'itérations effectuées
    return: NoneType
    '''
    couleurs = [(0, 200, 255),(0,255,0),(255,0,0)]
##    styles = ['o','8','4']

  
    pygame.init()
    fenetre = pygame.display.set_mode((NB_LIGNES*10, NB_COLONNES*10),RESIZABLE)
    
##    pylab.axis([-1, NB_LIGNES, -1, NB_COLONNES])
##    pylab.xlabel('',fontsize=0)
##    pylab.ylabel('',fontsize=0)
##    titre = 'Etat de la mer après '+str(nb_iter)+' itérations'
##    pylab.title(titre)
    for i in range(NB_LIGNES):
        for j in range(NB_COLONNES):
            k = voir_genre(mer,i,j)
            coul = couleurs[k]
##            mark = styles[k]
            carre = pygame.draw.rect(fenetre, coul, [10*j, 10*(NB_LIGNES-1-i), 9, 9],0)
##            if k==2 or k==0:
##                pylab.scatter(j, NB_LIGNES-1-i,s = 120, c='w')# pour l'esthétique...
##            pylab.scatter(j, NB_LIGNES-1-i,s = 100, c=coul, marker=mark)
##            pylab.pause(0.00000000000000001)# sans cela, pas d'affichage...
    pygame.display.flip()






def afficher_courbes(nb_total_iter):
    '''
    affiche un graphique montrant l'évolution du nombre de thons (courbe bleue)
    et du nombre de requins (courbe rouge) en fonction du temps (des itérations)
    params: nb_total_iter : le nombre total d'itérations
    return: NoneType
    '''
    abscisses = range(nb_total_iter)
    ordonnees_thons = list()
    ordonnees_requins = list()
    for etat in etats:
        ordonnees_thons.append(etat[0])
        ordonnees_requins.append(etat[1])
    pylab.plot(abscisses, ordonnees_thons, label='thons')
    pylab.plot(abscisses, ordonnees_requins, label='requins')
    pylab.legend(loc='upper right')
    pylab.title('Evolution des populations')
    pylab.show()


def compter_poissons(mer):
    '''
    compte et affiche le nombre de poissons dans la mer
    >>> ma_mer=[[2,0,2],[131,201,1],[411,1,1]]
    >>> compter_poissons(ma_mer)
    Il y a 5 thons et 3 requins.
    '''
    t,r=0,0
    for liste in mer:
        for val in liste:
            if val > 99:
                r += 1
            elif val > 0:
                t += 1
    print('Il y a',t,'thons et',r,'requins.')




def wator(p,q,n):
    global nb_thons,nb_requins
    '''
    Lance la simulation Wa-tor
    params:
    p et q sont les pourcentages initiaux de thons et de requins
    n est le nombre total d'itérations souhaité
    return:
    liste contenant le nombre de thons et de requins à chaque étape
    '''
    # création d'une mer vide
    ma_mer = creer_mer_vide(NB_LIGNES,NB_COLONNES)
    # peuplement avec p % de thons et q % de requins (environ...)
    peupler_mer(ma_mer,p,q)
    
    # nombre d'itérations entre deux affichages de la mer
    nb_iter_affich = n // 50
    
    # lancement des itérations
    for i in range(n):
        # choix d'une case au hasard
        (x,y) = choisir_case()
        # on regarde ce qu'il y a dedans : eau, thon ou requin
        genre = voir_genre(ma_mer,x,y)
        if genre == 1 :# si la case contient un thon
            comportement_thon(ma_mer,x,y)
        elif genre == 2 :# si la case contient un requin
            comportement_requin(ma_mer,x,y)
        etats.append([nb_thons,nb_requins])# enregistrement de l'état actuel de la mer
##        if i % nb_iter_affich == 0:# affichage de la mer
##            afficher_mer_visuel(ma_mer,i)# affichage graphique
            # affichage graphique
##            # ou afficher_mer_textuel(ma_mer,i) pour affichage dans console
        afficher_mer_pygame(ma_mer,i)
##    pylab.close()
##    pylab.pause(1)
    pygame.quit()
    afficher_courbes(n)
    compter_poissons(ma_mer)
    return etats
    
wator(30,10,1000)

testmod(verbose=False)
