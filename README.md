# AI Text Completion App

This is a simple Python app that lets you chat with AI models using the OpenRouter API. You can pick from several free and paid models, adjust creativity and response length, and try out different prompts. The app is designed for easy experimentation and learning.

## Features
- Chat with different AI models (Llama 3.2, Phi-3 Mini, Gemma 2, GPT-3.5, etc.)
- Choose creativity (temperature) and response length
- Use example prompts or type your own
- Simple command-line interface
- Includes an experiment runner for testing multiple prompts automatically

## OpenRouter Free Tier Explained

- **Free Credits:** When you sign up at [openrouter.ai](https://openrouter.ai), you get free credits automatically—no credit card required.
- **Free Models:** Many models have a free tier, including Llama 3.2, Phi-3 Mini, and Gemma 2. These are marked as "free" in the app's model selection.
- **Paid Models:** Some models are very cheap, but will use up your free credits. You can see your balance on the OpenRouter dashboard.
- **What happens when you run out?** If you use up your free credits, you can still use the free models, but paid models will stop working until you add more credits (as little as $1).
- **No credit card needed to start:** You can use all free models and your initial credits without entering payment info.


## Setup

1. **Install Python 3.8+** (if you don't have it already)
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Get a free API key:**
   - Go to [openrouter.ai](https://openrouter.ai) and sign up (no credit card needed)
   - Copy your API key from their dashboard
4. **Set your API key:**
   - Easiest: Create a file called `.env` in this folder and add this line:
     ```
     OPENROUTER_API_KEY=your-key-here
     ```
   - Or set it in your terminal:
     ```bash
     export OPENROUTER_API_KEY='your-key-here'
     ```

## Usage

### Start the app
```bash
python ai_text_completion.py
```
- Pick a model (just type 1, 2, 3, or 4)
- Adjust settings if you want (or press Enter for defaults)
- Type your prompt, or use an example by typing its number
- Type `exit` to quit, `help` for commands, or `settings` to change settings

### Run experiments
```bash
python experiment_runner.py
```
- This will automatically test 5 different prompts and show the results

## Example Prompts
- "Once upon a time, there was a robot who..."
- "Explain photosynthesis to a 10-year-old."
- "Write a haiku about the ocean."
- "What are the benefits of renewable energy?"
- "Explain recursion like I'm five."

## Troubleshooting
- **No API key found:** Make sure you set `OPENROUTER_API_KEY` in your `.env` file or environment
- **Can't connect:** Check your internet and API key
- **Not enough credits:** You used up your free credits; add a small amount to your OpenRouter account

## Project Structure
```
ai_text_completion.py      # Main app (all-in-one)
experiment_runner.py       # Automated prompt testing
requirements.txt           # Dependencies
README.md                  # This file
```

## Why use this?
- Free and easy to set up
- Great for learning about AI text generation
- Simple, readable code
- No extra dependencies

