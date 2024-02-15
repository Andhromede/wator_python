from .animal import Animal


class Shark(Animal):
    """
    Classe représentant un requin dans la simulation Wa-Tor.

    Les requins ont des comportements supplémentaires par rapport aux poissons, notamment la nécessité de manger
    pour survivre et un mécanisme de reproduction basé sur le nombre de poissons mangés plutôt que sur l'âge seul.
    """
    # def __init__(self, starve_time=3):
    #     # super().__init__(0)  # L'appel à super n'est plus nécessaire pour le temps de reproduction.
    #     self.starve_time = starve_time
    #     self.time_since_last_meal = 0
    #     self.fish_eaten = 0

    # def __init__(self, starve_time=3):
    #     """
    #     Initialise un nouveau requin avec un temps de reproduction et un temps avant de mourir de faim.

    #     :param breed_time: Nombre de tours nécessaires avant que le requin puisse se reproduire.
    #     :param starve_time: Nombre de tours après lesquels le requin meurt s'il n'a pas mangé.
    #     """
    #     super().__init__(0)  # On suppose que le temps de reproduction n'est pas utilisé pour les requins.
    #     self.starve_time = starve_time
    #     self.time_since_last_meal = 0
    #     self.fish_eaten = 0

    def __init__(self,  starve_time=5):
        # super().__init__(breed_time)  # breed_time n'est peut-être pas nécessaire selon votre logique
        self.starve_time = starve_time
        self.time_since_last_meal = 0
        self.fish_eaten = 0


    def increment_hunger(self):
        """
        Incrémente le temps écoulé depuis le dernier repas du requin.
        
        Cette méthode est appelée à chaque tour pour simuler l'augmentation de la faim.
        """
        self.time_since_last_meal += 1


    def reset_hunger(self):
        """
        Réinitialise le compteur de temps depuis le dernier repas du requin.

        Appelée lorsque le requin mange un poisson, simulant ainsi qu'il a été nourri.
        """
        self.time_since_last_meal = 0


    def is_starving(self):
        """
        Vérifie si le requin est affamé à mort (n'a pas mangé depuis `starve_time` tours).

        :return: True si le requin meurt de faim, False sinon.
        """
        return self.time_since_last_meal >= self.starve_time


    def increment_fish_eaten(self):
        """
        Incrémente le nombre de poissons mangés par le requin.

        Utilisée pour suivre le nombre de repas consommés et déterminer la capacité de reproduction.
        """
        self.fish_eaten += 1


    def can_breed(self):
        """
        Détermine si le requin peut se reproduire, basé sur le nombre de poissons mangés.

        :return: True si le requin a mangé au moins 3 poissons, False sinon.
        """
        return self.fish_eaten >= 3

    def reset_reproduction(self):
        """
        Réinitialise le compteur de poissons mangés après la reproduction.

        Permet au requin de commencer un nouveau cycle de reproduction après avoir donné naissance.
        """
        self.fish_eaten = 0
    