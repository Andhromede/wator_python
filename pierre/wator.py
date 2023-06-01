import math
import random
import time
from model.fish import Fish

grid = {}
largeur = 8
longueur = 15
listPoisson = []

for i in range(largeur):
    grid[i] = []
    for j in range(longueur):
        grid[i].append(" ")

def initFish(largeur,longueur,grid) -> list:
    nbPoisson = math.floor((longueur/3) * largeur)
    listPoisson = []
    for i in range(nbPoisson):
        ok = False
        while not(ok):
            largRandom = random.randrange(largeur)
            longRandom = random.randrange(longueur)
            caseSelect = grid[largRandom][longRandom]
            if caseSelect == " ":
                grid[largRandom][longRandom] = Fish([largRandom,longRandom])
                listPoisson.append(grid[largRandom][longRandom])
                ok = True
    return listPoisson

listPoisson = initFish(largeur,longueur,grid)

while True:
    for poisson in listPoisson:
        positions = poisson.move(grid)
        poisson.setPosition(positions[1])
        if poisson.gestation:
            poisson.setGestation(False)
        else:
            grid[positions[0][0]][positions[0][1]] = " "
        grid[positions[1][0]][positions[1][1]] = "§"

    print("_" * (len(grid[0]) + 2))
    for key, ligne in grid.items():
        textLigne = ""
        for col in ligne:
            textLigne += col if type(col) == str else col.symbol
        print(f"|{textLigne}|")
    time.sleep(1)