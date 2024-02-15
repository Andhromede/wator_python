class Animal:
    """
    Classe de base représentant un animal dans la simulation Wa-Tor.

    Chaque animal a un âge et un temps de reproduction spécifié (breed_time),
    qui détermine après combien de tours il est capable de se reproduire.
    """

    def __init__(self, breed_time):
        """
        Initialise un nouvel animal avec le temps nécessaire avant de pouvoir se reproduire.

        :param breed_time: Nombre de tours nécessaires avant que l'animal puisse se reproduire.
        """
        self.breed_time = breed_time    # Temps nécessaire pour se reproduire
        self.age = 0                    # Âge de l'animal

    def increment_age(self):
        """
        Incrémente l'âge de l'animal d'une unité.

        Cette méthode est appelée à chaque tour pour simuler le vieillissement de l'animal.
        """
        self.age += 1

    def reset_age(self):
        """
        Réinitialise l'âge de l'animal à 0.

        Typiquement appelée après la reproduction pour simuler le cycle de reproduction
        où l'animal doit attendre un nouveau cycle complet avant de pouvoir se reproduire à nouveau.
        """
        self.age = 0

    def can_breed(self):
        """
        Détermine si l'animal peut se reproduire.

        Un animal peut se reproduire s'il a atteint ou dépassé son temps de reproduction (breed_time).

        :return: True si l'animal peut se reproduire, False sinon.
        """
        return self.age >= self.breed_time