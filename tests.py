import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from agent import Agent
from simulation import World
from gemini_api import GeminiAPI
from report import ReportGenerator

class TestAgent(unittest.TestCase):
    def test_agent_initialization(self):
        agent = Agent(1, 0, 0)
        self.assertTrue(agent.alive)
        self.assertEqual(agent.x, 0)
        self.assertEqual(agent.y, 0)

    def test_agent_decide_action(self):
        agent = Agent(1, 0, 0, ethics=0.9)
        agent.hunger = 9
        action = agent.decide_action(None)
        self.assertIn(action, ["steal", "beg"])

    def test_agent_reproduce(self):
        world = MagicMock()
        world.is_in_bounds.return_value = True
        world.is_occupied.return_value = False
        world.get_next_agent_id.return_value = 2

        agent = Agent(1, 0, 0)
        agent.energy = 8
        agent.hunger = 2
        agent.reproduction_cooldown = 0

        child = agent.reproduce(world)
        self.assertIsNotNone(child)
        self.assertIsInstance(child, Agent)

class TestWorld(unittest.TestCase):
    def test_world_initialization(self):
        world = World(width=10, height=10, initial_agents=5)
        self.assertEqual(len(world.agents), 5)
        self.assertTrue(all(world.is_in_bounds(a.x, a.y) for a in world.agents))

    def test_world_update(self):
        world = World(width=10, height=10, initial_agents=2)
        initial_agent_count = len(world.agents)
        world.update()
        self.assertTrue(len(world.agents) >= 0)
        self.assertTrue(world.time == 1)

class TestGeminiAPI(unittest.TestCase):
    @patch('gemini_sim.gemini_api.genai.Client.models')
    def test_rate_society(self, mock_models):
        mock_generate = MagicMock()
        mock_generate.generate_content.return_value = MagicMock(text="7.5")
        mock_models.generate_content = mock_generate.generate_content

        api = GeminiAPI(api_key="fake_key")
        score = api.rate_society("Test society summary")
        self.assertEqual(score, 7.5)

    @patch('gemini_sim.gemini_api.genai.Client.models')
    def test_ask_policy_question(self, mock_models):
        mock_generate = MagicMock()
        mock_generate.generate_content.return_value = MagicMock(text="Yes, resource hoarding should be punished.")
        mock_models.generate_content = mock_generate.generate_content

        api = GeminiAPI(api_key="fake_key")
        answer = api.ask_policy_question("Should resource hoarding be punished?")
        self.assertIn("Yes", answer)

class TestReportGenerator(unittest.TestCase):
    def test_generate_report(self):
        reporter = ReportGenerator(output_dir="test_reports")
        text = "This is a test report."
        filepath = reporter.generate_report(text, filename="test_report.txt")
        self.assertTrue(os.path.exists(filepath))
        with open(filepath, "r") as f:
            content = f.read()
        self.assertEqual(content, text)
        # Clean up
        os.remove(filepath)
        os.rmdir("test_reports")

if __name__ == "__main__":
    unittest.main()
