# AI Mafia

AI Mafia is a text-based Mafia game where all players are controlled by large language models (LLMs). The game runs entirely in the terminal and requires API keys for the supported providers.

## Features
- Eight-player Mafia game with roles: 2 Mafia, 1 Doctor, 1 Sheriff, and 4 Town.
- Day and night cycles with speeches, votes, kills, heals, and investigations.
- Supports OpenAI Responses API plus OpenAI-compatible providers (DeepSeek, xAI Grok).
- Strict JSON prompts with automatic retry if the model returns invalid JSON.
- Memory and suspicion tracking for each AI-controlled agent.

## Requirements
- Python 3.10+
- API keys set as environment variables
  - `OPENAI_API_KEY`
  - `DEEPSEEK_API_KEY`
  - `XAI_API_KEY`
- Dependencies from `requirements.txt`

## Setup
1. Clone the repository and enter the project directory.
2. Create a virtual environment (recommended) and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in any provider keys you plan to use.
4. Run the game:
   ```bash
   python main.py
   ```

## Notes
- The game reads API keys **only** from environment variables. If a provider key is missing, that provider will not be used for player assignment.
- Model outputs are required to be valid JSON. If the response cannot be parsed, the game will request a one-time correction.
- Logs show all speeches, votes, night outcomes (without revealing roles), and the final role reveal.
