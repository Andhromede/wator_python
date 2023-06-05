import random

class Fish:

    nextId = 0
    symbol = "§"
    timeReproduction = 5

    def __init__(self,position) -> None:
        Fish.nextId += 1
        self.id = Fish.nextId
        self.nextReproduction = 5
        self.position = position
        self.gestation = False

    def move(self,grid) -> list:
        case_disponible = self.verifMovePossible(grid)
        nextPosition = self.position if case_disponible == [] else case_disponible[random.randrange(len(case_disponible))]
        if self.nextReproduction == 0:
            self.gestation = True
        self.nextReproduction = Fish.timeReproduction if self.nextReproduction == 0 else self.nextReproduction -1
        return [self.position,nextPosition]

    def verifMovePossible(self,grid) -> list:
        case_disponible = []
        case_a_regarder = {
            "haut": grid[(self.position[0] + 1) % len(grid)][self.position[1]],
            "bas": grid[(self.position[0] - 1) % len(grid)][self.position[1]],
            "droite": grid[self.position[0]][(self.position[1] + 1) % len(grid[0])],
            "gauche" : grid[self.position[0]][(self.position[1] - 1) % len(grid[0])]
        }

        if case_a_regarder["haut"] == ' ':
            case_disponible.append([(self.position[0] + 1) % len(grid),self.position[1]])
        if case_a_regarder["bas"] == ' ':
            case_disponible.append([(self.position[0] - 1) % len(grid),self.position[1]])
        if case_a_regarder["droite"] == ' ':
            case_disponible.append([self.position[0],(self.position[1] + 1) % len(grid[0])])
        if case_a_regarder["gauche"] == ' ':
            case_disponible.append([self.position[0],(self.position[1] - 1) % len(grid[0])])
        return case_disponible
    
    def reproduction():
        pass
        
    def setPosition(self,newPosition):
        self.position = newPosition

    def setGestation(self,gestation):
        self.gestation = gestation