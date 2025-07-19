import random
from agent import Agent

class World:
    def __init__(self, width=50, height=50, initial_agents=100):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(height)] for _ in range(width)]
        self.agents = []
        self.agent_id_counter = 0
        self.time = 0  # simulation time in steps

        # Initialize agents randomly on the grid
        for _ in range(initial_agents):
            x, y = self.get_random_empty_cell()
            if x is not None and y is not None:
                agent = Agent(self.get_next_agent_id(), x, y)
                self.agents.append(agent)
                self.grid[x][y] = agent

    def get_next_agent_id(self):
        self.agent_id_counter += 1
        return self.agent_id_counter

    def get_random_empty_cell(self):
        empty_cells = [(x, y) for x in range(self.width) for y in range(self.height) if self.grid[x][y] is None]
        if not empty_cells:
            return None, None
        return random.choice(empty_cells)

    def is_in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_occupied(self, x, y):
        return self.grid[x][y] is not None

    def update(self):
        """
        Run one simulation step: update agents, move, reproduce, and update grid.
        """
        self.time += 1

        # Clear grid for repositioning
        self.grid = [[None for _ in range(self.height)] for _ in range(self.width)]

        new_agents = []
        for agent in self.agents:
            if not agent.alive:
                continue

            agent.update(self)

            action = agent.decide_action(self)
            if action == "explore":
                agent.move(self)
            elif action == "rest":
                agent.energy = min(agent.energy + 3, 10)
            elif action == "steal":
                # Simple steal logic: try to steal from adjacent agents
                self.attempt_steal(agent)
            elif action == "beg":
                # Simple beg logic: gain small energy
                agent.energy = min(agent.energy + 1, 10)

            # Attempt reproduction
            child = agent.reproduce(self)
            if child:
                new_agents.append(child)

            # Update grid position
            if self.is_in_bounds(agent.x, agent.y):
                self.grid[agent.x][agent.y] = agent

        self.agents.extend(new_agents)

        # Remove dead agents
        self.agents = [a for a in self.agents if a.alive]

    def attempt_steal(self, thief):
        """
        Thief tries to steal energy from adjacent agents.
        """
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = thief.x + dx, thief.y + dy
            if self.is_in_bounds(nx, ny):
                victim = self.grid[nx][ny]
                if victim and victim.alive and victim.energy > 1:
                    stolen = min(2, victim.energy)
                    victim.energy -= stolen
                    thief.energy = min(thief.energy + stolen, 10)
                    break

    def get_summary(self):
        """
        Generate a summary of the current world state for reporting or Gemini queries.
        """
        total_agents = len(self.agents)
        if total_agents == 0:
            return "No agents alive."

        avg_ethics = sum(agent.ethics for agent in self.agents) / total_agents
        avg_selfishness = sum(agent.selfishness for agent in self.agents) / total_agents
        avg_curiosity = sum(agent.curiosity for agent in self.agents) / total_agents
        avg_energy = sum(agent.energy for agent in self.agents) / total_agents

        summary = (
            f"Time: {self.time} steps, Agents: {total_agents}, "
            f"Avg Ethics: {avg_ethics:.2f}, Avg Selfishness: {avg_selfishness:.2f}, "
            f"Avg Curiosity: {avg_curiosity:.2f}, Avg Energy: {avg_energy:.2f}"
        )
        return summary
