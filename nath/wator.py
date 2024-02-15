import random, time, os
from models.fish import Fish
from models.shark import Shark


class WaTorWorld:
    """
    La classe WaTorWorld simule un environnement aquatique où poissons et requins interagissent.
    """

    def __init__(self, width, height, num_fish, num_sharks):
        """
        Constructeur pour initialiser le monde Wa-Tor.

        :param width: largeur de la grille du monde
        :param height: hauteur de la grille du monde
        :param num_fish: nombre initial de poissons
        :param num_sharks: nombre initial de requins
        :param populate_world: nombre actuel de requins et de poissons
        """
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.num_fish = num_fish  # Initialiser avec le nombre initial de poissons
        self.num_sharks = num_sharks  # Initialiser avec le nombre initial de requins
        self.populate_world(num_fish, num_sharks)


    def display_world(self):
        """
        Affiche l'état actuel de la grille du monde.
        """
        for row in self.grid:
            row_display = ''
            for cell in row:
                if isinstance(cell, Fish):
                    row_display += '8 '
                elif isinstance(cell, Shark):
                    row_display += 'C '
                else:
                    row_display += '- '
            print(row_display)


    def populate_world(self, num_fish, num_sharks):
        """
        Peuple le monde avec un nombre spécifié de poissons et de requins placés aléatoirement.

        :param num_fish: nombre de poissons à placer
        :param num_sharks: nombre de requins à placer
        """
        positions = [(x, y) for x in range(self.width) for y in range(self.height)] # Créer une liste de toutes les positions possibles dans la grille
        random.shuffle(positions)               # Mélanger aléatoirement la liste pour obtenir une distribution aléatoire

        # Placer les poissons
        for _ in range(num_fish):
            if positions:                       # Vérifier s'il reste des positions disponibles
                x, y = positions.pop()          # Retirer une position de la liste
                self.grid[y][x] = Fish()        # Placer un poisson à cette position

        # Placer les requins
        for _ in range(num_sharks):             
            if positions:                       # Vérifier à nouveau pour les requins
                x, y = positions.pop()          # Retirer une autre position
                self.grid[y][x] = Shark()       # Placer un requin
                
        # super().populate_world(num_fish, num_sharks)


    def find_empty_nearby(self, x, y):
        """
        Trouve les cases vides adjacentes à une position spécifiée dans la grille.

        :param x: position en abscisse dans la grille
        :param y: position en ordonnée dans la grille
        :return: liste des positions vides adjacentes
        """
        empty_positions = []                                # Liste pour stocker les positions des cases vides adjacentes
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]     # Directions possibles pour chercher les cases adjacentes (Haut, Bas, Gauche, Droite)

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height:    # Vérifier si la nouvelle position est dans les limites de la grille
                if self.grid[new_y][new_x] is None:                     # Vérifier si la case est vide
                    empty_positions.append((new_x, new_y))

        return empty_positions


    def find_fish_nearby(self, x, y):
        """
        Cherche des poissons dans les cases adjacentes à une position spécifiée dans la grille.

        :param x: position en abscisse dans la grille
        :param y: position en ordonnée dans la grille
        :return: liste des positions des poissons trouvés
        """
        fish_positions = []                                 # Liste qui stocke les positions des poissons trouvés
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]     # Directions possibles pour chercher les cases adjacentes (Haut, Bas, Gauche, Droite)
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height:    # Vérifie si la nouvelle position est dans les limites de la grille
                if isinstance(self.grid[new_y][new_x], Fish):           # Vérifie si la case contient un poisson
                    fish_positions.append((new_x, new_y))

        return fish_positions


    def move_animal(self, x, y, new_x, new_y):
        """
        Déplace un animal de sa position actuelle vers une nouvelle position dans la grille.

        :param x: position en abscisse de départ dans la grille
        :param y: position en ordonnée de départ dans la grille
        :param new_x: position en abscisse d'arrivée dans la grille
        :param new_y: position en ordonnée d'arrivée dans la grille
        """
        if (x, y) != (new_x, new_y):                    # S'assurer que les positions de départ et d'arrivée sont différentes
            self.grid[new_y][new_x] = self.grid[y][x]   # Déplacer l'animal vers la nouvelle position
            self.grid[y][x] = None                      # Marquer l'ancienne position comme vide


    def move_fish(self, x, y, processed):
        """
        Déplace un poisson vers une case vide adjacente aléatoire et gère sa reproduction si les conditions sont remplies.

        :param x: position en abscisse du poisson dans la grille
        :param y: position en ordonnée du poisson dans la grille
        :param processed: un ensemble pour suivre les positions déjà traitées durant le tour
        """
        fish = self.grid[y][x]
        fish.increment_age()  # Incrémenter l'âge du poisson
        empty_nearby = self.find_empty_nearby(x, y)

        if empty_nearby:
            new_x, new_y = random.choice(empty_nearby)
            # Déplacer le poisson
            self.grid[y][x] = None
            self.grid[new_y][new_x] = fish
            processed.add((new_x, new_y))

            # Gérer la reproduction du poisson
            if fish.can_breed():
                fish.reset_age()
                self.grid[y][x] = Fish()  # Placer un nouveau poisson à l'ancienne position


    










    # def move_shark(self, x, y, processed):
    #     shark = self.grid[y][x]
    #     fish_nearby = self.find_fish_nearby(x, y)
    #     moved = False
    
    #     if fish_nearby:
    #         # Le requin mange le poisson et se déplace vers cette position
    #         new_x, new_y = random.choice(fish_nearby)
    #         self.grid[new_y][new_x] = shark
    #         shark.increment_fish_eaten()
    #         shark.reset_hunger()
    #         moved = True
    
    #         # Vérifie si le requin peut se reproduire après avoir mangé
    #         if shark.can_breed():
    #             shark.reset_reproduction()  # Réinitialise le compteur de poissons mangés
    #             if self.grid[y][x] is None:  # Vérifie si l'ancienne position est toujours vide
    #                 self.grid[y][x] = Shark(starve_time=shark.starve_time)
    #                 self.num_sharks += 1  # Mise à jour du compteur de requins seulement après la reproduction
    
    #         # Marque l'ancienne position du requin comme vide
    #         self.grid[y][x] = None
    
    #     if not moved:
    #         # Tentative de déplacement sans manger
    #         empty_nearby = self.find_empty_nearby(x, y)
    #         if empty_nearby:
    #             new_x, new_y = random.choice(empty_nearby)
    #             self.grid[new_y][new_x] = shark
    #             self.grid[y][x] = None
    #             moved = True
    
    #         # Incrémente le compteur de faim car le requin n'a pas mangé
    #         shark.increment_hunger()
    
    #     # Vérifie si le requin meurt de faim
    #     if shark.is_starving():
    #         if moved:
    #             self.grid[new_y][new_x] = None  # Enlève le requin de la nouvelle position s'il s'est déplacé
    #         else:
    #             self.grid[y][x] = None  # Enlève le requin de l'ancienne position s'il n'a pas bougé
    #         self.num_sharks -= 1  # Décrémente le nombre de requins
    #         return  # Termine la méthode tôt si le requin meurt
    
    #     # Marque la position comme traitée
    #     processed.add((new_x, new_y) if moved else (x, y))









    # def move_shark(self, x, y, processed):
    #     shark = self.grid[y][x]
    #     fish_nearby = self.find_fish_nearby(x, y)
    #     moved = False
    #     should_breed = shark.can_breed()  # Vérifie si le requin doit se reproduire avant de bouger

    #     # Déplacement du requin et gestion de l'alimentation
    #     if fish_nearby:
    #         new_x, new_y = random.choice(fish_nearby)
    #         self.grid[y][x] = None  # L'ancienne position devient vide
    #         self.grid[new_y][new_x] = shark  # Déplace le requin
    #         shark.increment_fish_eaten()  # Incrémente le nombre de poissons mangés
    #         shark.reset_hunger()  # Réinitialise la faim
    #         moved = True

    #         # Place un nouveau requin à l'ancienne position si les conditions de reproduction sont remplies
    #         if should_breed:
    #             shark.reset_reproduction()
    #             self.grid[y][x] = Shark(starve_time=shark.starve_time)
    #             self.num_sharks += 1

    #     # Gestion de la faim et de la mort par famine
    #     if not moved:
    #         shark.increment_hunger()
    #         if shark.is_starving():
    #             self.grid[y][x] = None
    #             self.num_sharks -= 1

    #     # Après avoir tenté de manger ou de se déplacer, incrémenter la faim du requin.
    #     if not fish_nearby:
    #         shark.increment_hunger()

    #     # Vérifier si le requin meurt de faim.
    #     if shark.is_starving():
    #         self.grid[y][x] = None                  # Retirer le requin de la grille s'il est mort de faim.
    #         self.num_sharks -= 1
    #         return                                  # Sortir de la fonction car le requin est mort.

    #     # Marquer la position comme traitée.
    #     processed.add((new_x, new_y) if moved else (x, y))






































    def move_shark(self, x, y, processed):
        """
        Permet au requin de chercher de la nourriture (poissons) dans les cases adjacentes,
        de se déplacer si aucune nourriture n'est trouvée, et se reproduit en laissant un nouveau
        requin dans la case qu'il vient de quitter après avoir mangé 3 poissons.
        """
        shark = self.grid[y][x]
        fish_nearby = self.find_fish_nearby(x, y)
        moved = False

        if fish_nearby:
            new_x, new_y = random.choice(fish_nearby)
            # self.grid[new_y][new_x] = None
            self.grid[new_y][new_x] = shark  # Déplace le requin vers le poisson et mange
            self.grid[y][x] = None if shark.fish_eaten < 2 else Shark(starve_time=shark.starve_time)  # Laisse un nouveau requin si les conditions sont remplies
            shark.increment_fish_eaten()
            shark.reset_hunger()
            moved = True

        if shark.can_breed():
            shark.reset_reproduction()
            # S'assure que l'ancienne case est vide avant d'y placer un nouveau requin.
            if self.grid[y][x] is None:
                self.grid[y][x] = Shark(starve_time=shark.starve_time)
                self.num_sharks += 1  # met à jour le compteur de requins.

        if not moved:
            empty_nearby = self.find_empty_nearby(x, y)
            if empty_nearby:
                new_x, new_y = random.choice(empty_nearby)
                self.grid[new_y][new_x] = shark
                self.grid[y][x] = None if not shark.can_breed() else Shark(starve_time=shark.starve_time)
                processed.add((new_x, new_y))

        if not moved:
            shark.increment_hunger()
            if shark.is_starving():
                self.grid[y][x] = None
















    def simulate_turn(self):
        """
        Simule un tour complet dans le monde Wa-Tor, impliquant :
        le déplacement des animaux, leur alimentation, leur reproduction 
        et en plus pour les requins, la gestion de leur survie en fonction de leur capacité à se nourrir.
    
        Chaque animal (poisson ou requin) sur la grille a la possibilité de se déplacer, de se reproduire
        ou de mourir de faim (dans le cas des requins) selon les règles spécifiques à son espèce.
        """
        processed = set()  # Crée une liste pour suivre les positions qui ont déjà été traitées
        positions = [(x, y) for x in range(self.width) for y in range(self.height)]  # Obtient la liste de toutes les positions et les mélange
        random.shuffle(positions)
    
        for x, y in positions:
            if (x, y) in processed:  # Si la position a déjà été traitée, passe à la suivante
                continue
            
            animal = self.grid[y][x]
            if animal is not None:
                # Détermine les actions en fonction du type d'animal
                if isinstance(animal, Shark):
                    self.move_shark(x, y, processed)
                elif isinstance(animal, Fish):
                    self.move_fish(x, y, processed)
            
            processed.add((x, y))  # Marque la position comme traitée
        
        # Réinitialisez les compteurs avant de les recalculer
        self.num_fish = 0
        self.num_sharks = 0
    
        # Parcourez la grille pour recompter les poissons et les requins
        for row in self.grid:
            for cell in row:
                if isinstance(cell, Fish):
                    self.num_fish += 1
                elif isinstance(cell, Shark):
                    self.num_sharks += 1

    
        # Affichez les compteurs mis à jour
        print(f"Nombre de poissons: {self.num_fish}")
        print(f"Nombre de requins: {self.num_sharks}")


    def run_simulation(self):
        """
        Exécute la simulation jusqu'à ce qu'une condition de terminaison soit atteinte :
        - Plus aucun poisson
        - Plus aucun requin
        - La grille est entièrement remplie
        """
        turn = 0  # Initialisation du compteur de tours
        while True:  # Boucle indéfiniment jusqu'à une condition de rupture
            os.system('cls' if os.name == 'nt' else 'clear')  # Efface la console
            turn += 1  # Incrémente le compteur de tours
            print(f"Tour {turn}")  # Affiche le numéro du tour
            print("\n" + "-"*20 + "\n")  # Ajoute une séparation visuelle
            
            self.simulate_turn()  # Simule un tour
            self.display_world()  # Affiche l'état actuel du monde
            time.sleep(1)  # Pause pour faciliter la visualisation
            
            # Vérifie les conditions de terminaison après la mise à jour de l'état du monde
            if not self.has_fish() or not self.has_shark() or self.is_grid_full():
                print("Simulation terminée.")
                break  # Sort de la boucle si une condition de terminaison est atteinte


    def has_fish(self):
        """
        Vérifie s'il reste des poissons dans la grille.

        :return: True s'il y a au moins un poisson, False sinon.
        """
        return any(isinstance(cell, Fish) for row in self.grid for cell in row)


    def has_shark(self):
        """
        Vérifie s'il reste des requins dans la grille.

        :return: True s'il y a au moins un requin, False sinon.
        """
        return any(isinstance(cell, Shark) for row in self.grid for cell in row)


    def is_grid_full(self):
        """
        Vérifie si la grille est complètement remplie (aucune cellule vide).

        :return: True si la grille est pleine, False sinon.
        """
        return all(cell is not None for row in self.grid for cell in row)


    def display_world(self):
        """
        Affiche l'état actuel de la grille du monde Wa-Tor.

        Chaque cellule de la grille peut être vide, contenir un poisson, ou contenir un requin.
        Les poissons sont représentés par '8', les requins par 'C', et les cases vides par '-'.
        Cette représentation visuelle permet de suivre facilement les interactions et les mouvements
        des poissons et des requins au sein de l'écosystème simulé.
        """
        for row in self.grid:
            row_display = ''
            for cell in row:
                if isinstance(cell, Fish):
                    row_display += '8 '
                elif isinstance(cell, Shark):
                    row_display += 'C '
                else:
                    row_display += '- '
            print(row_display)


# Initialiser le monde Wa-Tor avec une grille de dimensions spécifiques, un nombre initial de poissons et de requins.
# Cet exemple crée un monde de 15x15 cases, peuplé de 20 poissons et 5 requins, puis lance la simulation pour 50 tours.
if __name__ == "__main__":

    # Création d'une instance de WaTorWorld avec une grille de 15x15,
    # 20 poissons et 5 requins pour initialiser l'environnement de la simulation.
    world = WaTorWorld(15, 15, 20, 5)

    # Affichage de l'état initial du monde pour permettre à l'utilisateur
    # de voir la configuration de départ avant le début de la simulation.
    world.display_world()

    # Lancement de la simulation Wa-Tor pour un total de 50 tours. Cette fonction
    # va simuler le comportement des poissons et des requins, incluant leur mouvement,
    # alimentation, reproduction, et pour les requins, leur survie basée sur l'alimentation.
    # L'état du monde est affiché après chaque tour, permettant de suivre l'évolution de la simulation.
    world.run_simulation()
