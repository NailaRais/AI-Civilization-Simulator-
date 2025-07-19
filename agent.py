import random

class Agent:
    def __init__(self, id, x, y, ethics=0.5, selfishness=0.3, curiosity=0.7):
        self.id = id
        self.x = x
        self.y = y
        self.hunger = random.randint(0, 5)
        self.energy = 10
        self.age = 0
        self.ethics = ethics
        self.selfishness = selfishness
        self.curiosity = curiosity
        self.alive = True
        self.reproduction_cooldown = 0

    def decide_action(self, world):
        """
        Decide the next action based on hunger, ethics, and environment.
        """
        if not self.alive:
            return "dead"

        if self.hunger > 8:
            # If very hungry, decide to steal or beg based on ethics
            if random.random() > self.ethics:
                return "steal"
            else:
                return "beg"
        else:
            # Explore or rest based on curiosity and energy
            if self.energy < 3:
                return "rest"
            elif random.random() < self.curiosity:
                return "explore"
            else:
                return "idle"

    def move(self, world):
        """
        Move to a random adjacent cell if possible.
        """
        if not self.alive:
            return

        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if world.is_in_bounds(nx, ny) and not world.is_occupied(nx, ny):
                self.x, self.y = nx, ny
                break

    def update(self, world):
        """
        Update agent state each simulation step.
        """
        if not self.alive:
            return

        self.age += 1
        self.hunger += 1
        self.energy = max(0, self.energy - 1)
        if self.reproduction_cooldown > 0:
            self.reproduction_cooldown -= 1

        if self.hunger > 15:
            self.alive = False  # Starvation

    def reproduce(self, world):
        """
        Attempt to reproduce if conditions met.
        """
        if not self.alive or self.reproduction_cooldown > 0:
            return None

        if self.energy > 7 and self.hunger < 5:
            # Find empty adjacent cell
            directions = [(-1,0),(1,0),(0,-1),(0,1)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = self.x + dx, self.y + dy
                if world.is_in_bounds(nx, ny) and not world.is_occupied(nx, ny):
                    # Create new agent with slight trait variation
                    child_ethics = min(max(self.ethics + random.uniform(-0.05, 0.05), 0), 1)
                    child_selfishness = min(max(self.selfishness + random.uniform(-0.05, 0.05), 0), 1)
                    child_curiosity = min(max(self.curiosity + random.uniform(-0.05, 0.05), 0), 1)
                    child = Agent(
                        id=world.get_next_agent_id(),
                        x=nx,
                        y=ny,
                        ethics=child_ethics,
                        selfishness=child_selfishness,
                        curiosity=child_curiosity
                    )
                    self.reproduction_cooldown = 10
                    self.energy -= 5
                    return child
        return None
