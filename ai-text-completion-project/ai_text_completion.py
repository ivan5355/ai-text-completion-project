#!/usr/bin/env python3
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    return os.getenv('OPENROUTER_API_KEY')

def validate_prompt(prompt):
    if not prompt.strip():
        return False, "Please enter something."
    if len(prompt) > 2000:
        return False, "That's too long. Keep it under 2000 characters."
    return True, ""

def get_settings():
    print("\nSettings (press Enter for defaults):")
    
    try:
        temp = input("Creativity (0.1-1.5, default 0.7): ").strip()
        temperature = float(temp) if temp else 0.7
        if temperature < 0.1 or temperature > 1.5:
            temperature = 0.7
    except:
        temperature = 0.7
    
    try:
        tokens = input("Response length (50-500, default 200): ").strip()
        max_tokens = int(tokens) if tokens else 200
        if max_tokens < 50 or max_tokens > 500:
            max_tokens = 200
    except:
        max_tokens = 200
    
    return {'temperature': temperature, 'max_tokens': max_tokens}

def print_response(response, model_name):
    print(f"\n" + "="*50)
    print(f"Response from {model_name}:")
    print("="*50)
    print(response)
    print("="*50)

def show_error(error):
    error_text = str(error).lower()
    
    if 'api key' in error_text:
        print("\nError: API key problem. Check your OPENROUTER_API_KEY.")
    elif 'rate limit' in error_text:
        print("\nError: Too many requests. Wait and try again.")
    elif 'credits' in error_text:
        print("\nError: Not enough credits.")
    elif 'connection' in error_text:
        print("\nError: Can't connect to internet.")
    else:
        print(f"\nError: {error}")

def show_welcome():
    print("\n" + "="*50)
    print("         AI Text Completion App")
    print("="*50)

class AIChat:
    def __init__(self, model_name="meta-llama/llama-3.2-3b-instruct:free"):
        self.model_name = model_name
        self.api_key = get_api_key()
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        
        if not self.api_key:
            raise Exception("No API key found.")
        
        print(f"Using: {model_name}")
    
    def get_response(self, prompt, settings):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": settings['temperature'],
            "max_tokens": settings['max_tokens']
        }
        
        try:
            response = requests.post(self.url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                raise Exception(f"API error: {response.status_code}")
                
        except requests.RequestException as e:
            raise Exception(f"Connection error: {e}")

def choose_model():
    models = {
        "1": ("meta-llama/llama-3.2-3b-instruct:free", "Llama 3.2 (Free)"),
        "2": ("microsoft/phi-3-mini-128k-instruct:free", "Phi-3 Mini (Free)"),
        "3": ("google/gemma-2-9b-it:free", "Gemma 2 (Free)"),
        "4": ("openai/gpt-3.5-turbo", "GPT-3.5 (Cheap)")
    }
    
    print("\nPick a model:")
    for key, (_, name) in models.items():
        print(f"{key}. {name}")
    
    choice = input("\nWhich one? (1-4, default 1): ").strip()
    if choice in models:
        model_id, name = models[choice]
        print(f"Selected: {name}")
        return model_id
    else:
        return models["1"][0]

def test_connection():
    api_key = get_api_key()
    if not api_key:
        return False
    
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": "meta-llama/llama-3.2-3b-instruct:free",
        "messages": [{"role": "user", "content": "Hi"}],
        "max_tokens": 5
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers, json=data, timeout=10
        )
        return response.status_code == 200
    except:
        return False

def main():
    show_welcome()
    
    if not get_api_key():
        print("\nYou need an API key.")
        print("1. Sign up at https://openrouter.ai")
        print("2. Set OPENROUTER_API_KEY in .env file")
        return
    
    print("Testing connection...")
    if not test_connection():
        print("Can't connect. Check your API key.")
        return
    print("Connected!")
    
    model = choose_model()
    
    try:
        ai = AIChat(model)
    except Exception as e:
        show_error(e)
        return
    
    settings = get_settings()
    
    print(f"\nReady! Type 'exit' to quit.")
    
    examples = [
        "Once upon a time, there was a robot who...",
        "Explain photosynthesis to a 10-year-old.",
        "Write a haiku about the ocean.",
        "What are the benefits of renewable energy?",
        "Explain recursion like I'm five."
    ]
    
    print("\nExample prompts (type 1-5):")
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
    
    while True:
        try:
            user_input = input("\nYour prompt: ").strip()
            
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            elif user_input.lower() == 'help':
                print("\nCommands: exit, settings, help")
                continue
            elif user_input.lower() == 'settings':
                settings = get_settings()
                continue
            elif user_input.isdigit() and 1 <= int(user_input) <= len(examples):
                user_input = examples[int(user_input) - 1]
                print(f"Using: {user_input}")
            
            is_valid, error_msg = validate_prompt(user_input)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            print("\nThinking...")
            response = ai.get_response(user_input, settings)
            print_response(response, ai.model_name)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            show_error(e)

if __name__ == "__main__":
    main() 