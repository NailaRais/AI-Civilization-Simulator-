import pygame
import sys
import argparse
import time

from simulation import World
from gemini_api import GeminiAPI
from report import ReportGenerator

# Constants for display
CELL_SIZE = 10
GRID_COLOR = (200, 200, 200)
AGENT_COLOR = (0, 128, 255)
DEAD_AGENT_COLOR = (128, 128, 128)
BACKGROUND_COLOR = (255, 255, 255)

class Simulator:
    def __init__(self, width=50, height=50, initial_agents=100, use_gemini=False, api_key=None):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width * CELL_SIZE, height * CELL_SIZE))
        pygame.display.set_caption("AI Civilization Simulator")
        self.clock = pygame.time.Clock()
        self.world = World(width, height, initial_agents)
        self.use_gemini = use_gemini
        self.gemini = GeminiAPI(api_key) if use_gemini else None
        self.reporter = ReportGenerator()
        self.font = pygame.font.SysFont("Arial", 14)
        self.last_gemini_check = 0
        self.gemini_interval = 10  # simulation steps between Gemini queries

    def draw_grid(self):
        for x in range(self.width):
            for y in range(self.height):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

    def draw_agents(self):
        for agent in self.world.agents:
            color = AGENT_COLOR if agent.alive else DEAD_AGENT_COLOR
            rect = pygame.Rect(agent.x * CELL_SIZE, agent.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, color, rect)

    def display_text(self, text, x, y):
        surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(surface, (x, y))

    def run(self):
        running = True
        step = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.world.update()
            step += 1

            self.screen.fill(BACKGROUND_COLOR)
            self.draw_grid()
            self.draw_agents()

            summary = self.world.get_summary()
            self.display_text(summary, 5, 5)

            if self.use_gemini and step - self.last_gemini_check >= self.gemini_interval:
                self.last_gemini_check = step
                score = self.gemini.rate_society(summary)
                if score is not None:
                    score_text = f"Gemini Ethics Score: {score:.1f}"
                else:
                    score_text = "Gemini Ethics Score: N/A"
                self.display_text(score_text, 5, 25)

                # Generate and save report every Gemini check
                report_path = self.reporter.generate_report(f"{summary}\n{score_text}")
                print(f"Report saved to {report_path}")

            pygame.display.flip()
            self.clock.tick(10)  # 10 FPS

        pygame.quit()
        sys.exit()

def parse_args():
    parser = argparse.ArgumentParser(description="AI Civilization Simulator")
    parser.add_argument("--gemini", action="store_true", help="Enable Gemini API integration")
    parser.add_argument("--api_key", type=str, default=None, help="Gemini API key")
    parser.add_argument("--width", type=int, default=50, help="World width")
    parser.add_argument("--height", type=int, default=50, help="World height")
    parser.add_argument("--agents", type=int, default=100, help="Initial number of agents")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    sim = Simulator(
        width=args.width,
        height=args.height,
        initial_agents=args.agents,
        use_gemini=args.gemini,
        api_key=args.api_key
    )
    sim.run()
