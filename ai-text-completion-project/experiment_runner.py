#!/usr/bin/env python3
"""
Simple experiment runner to test different prompts
"""

import json
import time
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    return os.getenv('OPENROUTER_API_KEY')

def show_error(error):
    print(f"\nError: {error}")

class AIChat:
    def __init__(self, model_name="meta-llama/llama-3.2-3b-instruct:free"):
        self.model_name = model_name
        self.api_key = get_api_key()
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        
        if not self.api_key:
            raise Exception("No API key found.")
    
    def get_response(self, prompt, settings):
        import requests
        
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
        
        response = requests.post(self.url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            raise Exception(f"API error: {response.status_code}")

def run_experiments():
    """Run some basic experiments with different prompts."""
    
    if not get_api_key():
        print("You need an API key. Set OPENROUTER_API_KEY first.")
        return
    
    print("Starting experiments...")
    
    # Use a free model for testing
    model = "meta-llama/llama-3.2-3b-instruct:free"
    
    try:
        ai = AIChat(model)
    except Exception as e:
        show_error(e)
        return
    
    # Test prompts from the assignment
    test_prompts = [
        {
            "name": "Creative Story",
            "prompt": "Once upon a time, there was a robot who discovered they could feel emotions.",
            "settings": {"temperature": 0.8, "max_tokens": 200}
        },
        {
            "name": "Simple Explanation", 
            "prompt": "Explain photosynthesis to a 10-year-old.",
            "settings": {"temperature": 0.3, "max_tokens": 150}
        },
        {
            "name": "Poetry",
            "prompt": "Write a haiku about the ocean.",
            "settings": {"temperature": 0.9, "max_tokens": 100}
        },
        {
            "name": "Information",
            "prompt": "Summarize the main benefits of renewable energy sources.",
            "settings": {"temperature": 0.2, "max_tokens": 200}
        },
        {
            "name": "Technical Explanation",
            "prompt": "Explain recursion in programming like I'm five years old.",
            "settings": {"temperature": 0.4, "max_tokens": 150}
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_prompts, 1):
        print(f"\nTest {i}/{len(test_prompts)}: {test['name']}")
        print(f"Prompt: {test['prompt']}")
        
        start_time = time.time()
        
        try:
            response = ai.get_response(test['prompt'], test['settings'])
            end_time = time.time()
            
            result = {
                "test_name": test['name'],
                "prompt": test['prompt'],
                "response": response,
                "settings": test['settings'],
                "time_taken": round(end_time - start_time, 2),
                "success": True
            }
            
            print(f"Response: {response[:100]}...")
            print(f"Time: {result['time_taken']}s")
            
        except Exception as e:
            end_time = time.time()
            result = {
                "test_name": test['name'], 
                "prompt": test['prompt'],
                "response": None,
                "settings": test['settings'],
                "time_taken": round(end_time - start_time, 2),
                "success": False,
                "error": str(e)
            }
            
            print(f"Failed: {e}")
        
        results.append(result)
        
        # Wait a bit between requests
        time.sleep(1)
    
    # Show summary
    print(f"\n" + "="*50)
    print("EXPERIMENT RESULTS")
    print("="*50)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"Total tests: {len(results)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    
    if successful:
        avg_time = sum(r['time_taken'] for r in successful) / len(successful)
        print(f"Average response time: {avg_time:.2f}s")
    
    print(f"\nDetailed Results:")
    print("-" * 50)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['test_name']}")
        
        if result['success']:
            print(f"   Response length: {len(result['response'])} characters")
            print(f"   Time: {result['time_taken']}s")
            print(f"   Settings: Creativity={result['settings']['temperature']}, Length={result['settings']['max_tokens']}")
            
            # Simple quality check
            response_len = len(result['response'])
            if response_len < 30:
                print("   Note: Response seems short")
            elif response_len > 400:
                print("   Note: Response is quite long")
            else:
                print("   Note: Response length looks good")
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"experiment_results_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {filename}")
    except Exception as e:
        print(f"Couldn't save results: {e}")
    
    print("\nExperiment complete!")

def main():
    print("Simple AI Experiment Runner")
    print("=" * 40)
    print("This will test 5 different prompts and show the results.")
    
    choice = input("\nRun experiments? (y/n): ").strip().lower()
    if choice == 'y' or choice == 'yes' or choice == '':
        run_experiments()
    else:
        print("Okay, maybe next time!")

if __name__ == "__main__":
    main() 