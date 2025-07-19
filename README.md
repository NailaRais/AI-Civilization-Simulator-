# Ultra-Low-Cost AI Civilization Simulator Using Gemini API (Free Tier)

This project is an AI civilization simulator that runs a 2D grid world with agents exhibiting simple behaviors. It integrates with the Google Gemini API free tier to evaluate society ethics, teach agents, suggest policy changes, and generate reports.

## Features

- Local simulation of agents with traits like ethics, selfishness, and curiosity.
- Agents perform actions like moving, stealing, begging, resting, and reproducing.
- Integration with Gemini API for ethics evaluation and policy guidance.
- Automated report generation.
- Visualization using Pygame.
- Designed to run on zero cost using Gemini free tier and optionally deploy on Google Colab.

## Setup

1. Clone the repository or copy the project files.

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your Gemini API key as an environment variable:

```bash
export GEMINI_API_KEY="your_api_key_here"
```

Or pass it as a command line argument `--api_key`.

## Usage

Run the simulation locally without Gemini integration:

```bash
python world.py
```

Run the simulation with Gemini API integration:

```bash
python world.py --gemini
```

Specify Gemini API key explicitly:

```bash
python world.py --gemini --api_key YOUR_API_KEY
```

Adjust world size and initial agents:

```bash
python world.py --width 60 --height 60 --agents 150
```

## Running Tests

To run the automated test suite covering core functionality and Gemini API integration:

```bash
python -m unittest tests.py
```

## Deployment Options (Free)

- **GitHub:** Push the project to a GitHub repository. Use GitHub Actions for CI/CD if needed.
- **Google Colab:** Upload the project files to Colab, install dependencies, and run `world.py` in a notebook cell. Set GEMINI_API_KEY in environment variables.
- **Kaggle:** Upload the project as a Kaggle notebook or dataset. Use Kaggle's Python environment to run simulations and visualize results.

## Notes

- The simulation runs at 10 FPS and updates agent states each step.
- Gemini API is queried every 10 simulation steps for ethics rating.
- Reports are saved in the `reports/` directory.
- Designed for experimentation with AI-driven societal simulations.

## License

MIT License
python world.py --gemini --api_key YOUR_API_KEY
