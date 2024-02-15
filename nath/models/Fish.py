from .animal import Animal


class Fish(Animal):
    """
    Classe représentant un poisson dans la simulation Wa-Tor.

    Le poisson a un âge et un âge spécifique à partir duquel il peut se reproduire (breed_age).
    L'héritage de la classe Animal permet de réutiliser la logique commune à tous les animaux,
    telle que la gestion de l'âge et de la reproduction.
    """

    def __init__(self, breed_age=10):
        """
        Initialise un nouveau poisson avec un âge de reproduction spécifié.

        :param breed_age: Âge auquel le poisson est capable de se reproduire.
                          La valeur par défaut est 10, mais peut être ajustée selon les besoins de la simulation.
        """
        # Appelle le constructeur de la classe parent (Animal) avec le temps nécessaire pour se reproduire.
        super().__init__(breed_age)
        

        