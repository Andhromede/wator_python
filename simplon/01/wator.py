import random
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

EMPTY = 0
FISH = 1
SHARK = 2

# Colour the cells for the above states in this order:
colors = ['#00008b', '#ff69b4', '#ffd700']
n_bin = 3
cm = LinearSegmentedColormap.from_list(
        'wator_cmap', colors, N=n_bin)

# Run the simulation for MAX_CHRONONS chronons (time intervals).
MAX_CHRONONS = 400
# Save every SAVE_EVERYth chronon iteration.
SAVE_EVERY = 5
# PRNG seed.
SEED = 10
random.seed(SEED)

initial_energies = {FISH: 20, SHARK: 3}
fertility_thresholds = {FISH: 4, SHARK: 12}

class Creature():
    """A sea creature living in Wa-Tor world."""

    def __init__(self, id, x, y, init_energy, fertility_threshold):
        """Initialize the creature.

        id is an integer identifying the creature.
        x, y is the creature's position in the Wa-Tor world grid.
        init_energy is the creature's initial energy: this decreases by 1
            each time the creature moves and if it reaches 0 the creature dies.
        fertility_threshold: each chronon, the creature's fertility increases
            by 1. When it reaches fertility_threshold, the creature reproduces.

        """

        self.id = id
        self.x, self.y = x, y
        self.energy = init_energy
        self.fertility_threshold = fertility_threshold
        self.fertility = 0
        self.dead = False


class World():
    """The Wa-Tor world."""

    def __init__(self, width=75, height=50):
        """Initialize (but don't populate) the Wa-Tor world."""

        self.width, self.height = width, height
        self.ncells = width * height
        self.grid = [[EMPTY]*width for y in range(height)]
        self.creatures = []

    def spawn_creature(self, creature_id, x, y):
        """Spawn a creature of type ID creature_id at location x,y."""

        creature = Creature(creature_id, x, y,
                            initial_energies[creature_id],
                            fertility_thresholds[creature_id])
        self.creatures.append(creature)
        self.grid[y][x] = creature

    def populate_world(self, nfish=120, nsharks=40):
        """Populate the Wa-Tor world with fish and sharks."""

        self.nfish, self.nsharks = nfish, nsharks

        def place_creatures(ncreatures, creature_id):
            """Place ncreatures of type ID creature_id in the Wa-Tor world."""

            for i in range(ncreatures):
                while True:
                    x, y = divmod(random.randrange(self.ncells), self.height)
                    if not self.grid[y][x]:
                        self.spawn_creature(creature_id, x, y)
                        break

        place_creatures(self.nfish, FISH)
        place_creatures(self.nsharks, SHARK)

    def get_world_image_array(self):
        """Return a 2D array of creature type IDs from the world grid."""
        return [[self.grid[y][x].id if self.grid[y][x] else 0
                    for x in range(self.width)] for y in range(self.height)]

    def get_world_image(self):
        """Create a Matplotlib figure plotting the world."""

        im =  self.get_world_image_array()
        fig = plt.figure(figsize=(8.3333, 6.25), dpi=72)
        ax = fig.add_subplot(111)
        ax.imshow(im, interpolation='nearest', cmap=cm)

        # Remove ticks, border, axis frame, etc
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')
        return fig

    def show_world(self):
        """Show the world as a Matplotlib image."""

        fig = self.get_world_image()
        plt.show()
        plt.close(fig)

    def save_world(self, filename):
        """Save a Matplotlib image of the world as filename."""

        fig = self.get_world_image()
        # NB Ensure there's no padding around the image plot
        plt.savefig(filename, dpi=72, bbox_inches='tight', pad_inches=0)
        plt.close(fig)

    def get_neighbours(self, x, y):
        """Return a dictionary of the contents of cells neighbouring (x,y).

        The dictionary is keyed by the neighbour cell's position and contains
        either EMPTY or the instance of the creature occupying that cell.

        """

        neighbours = {}
        for dx, dy in ((0,-1), (1,0), (0,1), (-1,0)):
            xp, yp = (x+dx) % self.width, (y+dy) % self.height
            neighbours[xp,yp] = self.grid[yp][xp]
        return neighbours

    def evolve_creature(self, creature):
        """Evolve a given creature forward in time by one chronon."""

        neighbours = self.get_neighbours(creature.x, creature.y)
        creature.fertility += 1
        moved = False
        if creature.id == SHARK:
            try:
                # Try to pick a random fish to eat.
                xp, yp = random.choice([pos
                            for pos in neighbours if neighbours[pos]!=EMPTY
                                                and neighbours[pos].id==FISH])
                # Eat the fish. Yum yum.
                creature.energy += 2
                self.grid[yp][xp].dead = True
                self.grid[yp][xp] = EMPTY
                moved = True
            except IndexError:
                # No fish to eat: just move to a vacant cell if possible.
                pass

        if not moved:
            # Try to move to a vacant cell
            try:
                xp, yp = random.choice([pos
                            for pos in neighbours if neighbours[pos]==EMPTY])
                if creature.id != FISH:
                    # The shark's energy decreases by one unit when it moves.
                    creature.energy -= 1
                moved = True
            except IndexError:
                # Surrounding cells are all full: no movement.
                xp, yp = creature.x, creature.y

        if creature.energy < 0:
            # Creature dies.
            creature.dead = True
            self.grid[creature.y][creature.x] = EMPTY
        elif moved:
            # Remember the creature's old position.
            x, y = creature.x, creature.y
            # Set new position
            creature.x, creature.y = xp, yp
            self.grid[yp][xp] = creature
            if creature.fertility >= creature.fertility_threshold:
                # Spawn a new creature and reset fertility.
                creature.fertility = 0
                self.spawn_creature(creature.id, x, y)
            else:
                # Leave the old cell vacant.
                self.grid[y][x] = EMPTY

    def evolve_world(self):
        """Evolve the Wa-Tor world forward in time by one chronon."""

        # Shuffle the creatures grid so that we don't always evolve the same
        # creatures first.
        random.shuffle(self.creatures)

        # NB The self.creatures list is going to grow as new creatures are
        # spawned, so loop over indices into the list as it stands now.
        ncreatures = len(self.creatures)
        for i in range(ncreatures):
            creature = self.creatures[i]
            if creature.dead:
                # This creature has been eaten so skip it.
                continue
            self.evolve_creature(creature)

        # Remove the dead creatures
        self.creatures = [creature for creature in self.creatures
                                                if not creature.dead]

world = World()
world.populate_world()
for chronon in range(400):
    if not chronon % SAVE_EVERY:
        print('{}/{}: {}'.format(chronon+1,MAX_CHRONONS, len(world.creatures)))
        world.save_world('world-{:04d}.png'.format(chronon))
    world.evolve_world()