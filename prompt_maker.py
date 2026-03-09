#!/usr/bin/env python3
"""
Prompt Generator for Kirsche Pictures

This script generates random prompts for picture generation by selecting
random elements from predefined lists of outfits, locations, activities,
and emotions. The generated prompt is then enhanced using a local Ollama
instance for more creative and detailed results.
"""

import random
import requests
import json


# Predefined elements for prompt generation
outfits_elements = [
    "a flowing red dress",
    "a cozy winter jacket",
    "a traditional kimono",
    "casual jeans and a t-shirt",
    "an elegant evening gown",
    "athletic workout gear",
    "a futuristic space suit",
    "a cute summer sundress",
    "a professional business suit",
    "a comfy hoodie and sweatpants",
    "a steampunk outfit with goggles",
    "a vintage 1950s dress",
    "a fantasy warrior armor",
    "a beach swimsuit",
    "a punk rock leather jacket",
    "a magical girl outfit",
    "a bohemian flowing skirt",
    "a cyberpunk neon jacket",
    "a medieval princess gown",
    "pajamas with cute patterns"
]

locations_elements = [
    "a sunny park",
    "the beach at sunset",
    "outer space",
    "a cozy coffee shop",
    "a magical forest",
    "a bustling city street",
    "a snowy mountain peak",
    "an underwater coral reef",
    "a futuristic cityscape",
    "a peaceful garden",
    "an ancient temple",
    "a desert oasis",
    "a floating island in the sky",
    "a Gothic cathedral",
    "a neon-lit arcade",
    "a cherry blossom grove",
    "a steampunk airship",
    "a haunted mansion",
    "a tropical rainforest",
    "a starlit rooftop"
]

activities_elements = [
    "reading a book",
    "painting a canvas",
    "playing video games",
    "stargazing",
    "having a picnic",
    "dancing",
    "practicing martial arts",
    "playing guitar",
    "taking photographs",
    "meditating",
    "baking cookies",
    "flying a kite",
    "exploring ruins",
    "skateboarding",
    "writing in a journal",
    "playing with pets",
    "doing yoga",
    "building a sandcastle",
    "singing karaoke",
    "creating digital art"
]

emotions_elements = [
    "joyful",
    "peaceful",
    "excited",
    "contemplative",
    "confident",
    "playful",
    "serene",
    "adventurous",
    "mischievous",
    "proud",
    "inspired",
    "dreamy",
    "energetic",
    "content",
    "curious",
    "determined",
    "whimsical",
    "relaxed",
    "enthusiastic",
    "mysterious"
]


def generate_prompt():
    """
    Generate a random prompt by selecting one element from each category.
    
    Returns:
        str: The generated prompt string
    """
    outfit = random.choice(outfits_elements)
    location = random.choice(locations_elements)
    activity = random.choice(activities_elements)
    emotion = random.choice(emotions_elements)
    
    prompt = (
        f"Draw a picture of Kirsche wearing {outfit} in {location}. "
        f"She is engaged in {activity} and feeling {emotion}."
    )
    
    return prompt


def enhance_prompt_with_ollama(prompt, model="llama3.2", ollama_url="http://localhost:11434"):
    """
    Enhance the generated prompt using a local Ollama instance.
    
    Args:
        prompt (str): The original prompt to enhance
        model (str): The Ollama model to use (default: llama3.2)
        ollama_url (str): The Ollama API endpoint URL (default: http://localhost:11434)
    
    Returns:
        str: The enhanced prompt, or the original prompt if enhancement fails
    """
    enhancement_instruction = (
        f"You are a creative prompt enhancer. Take the following image generation prompt "
        f"and make it more creative, detailed, and vivid while keeping it PG-rated. "
        f"Maintain the core structure and elements but add artistic details, atmosphere, "
        f"lighting, composition, and style elements. Return ONLY the enhanced prompt, "
        f"nothing else.\n\nOriginal prompt: {prompt}"
    )
    
    try:
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": model,
                "prompt": enhancement_instruction,
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            enhanced_prompt = result.get("response", "").strip()
            
            if enhanced_prompt:
                print(f"\n✓ Prompt enhanced successfully using {model}")
                return enhanced_prompt
            else:
                print(f"\n⚠ Warning: Ollama returned empty response, using original prompt")
                return prompt
        else:
            print(f"\n⚠ Warning: Ollama API returned status {response.status_code}, using original prompt")
            return prompt
            
    except requests.exceptions.ConnectionError:
        print(f"\n⚠ Warning: Could not connect to Ollama at {ollama_url}, using original prompt")
        return prompt
    except requests.exceptions.Timeout:
        print(f"\n⚠ Warning: Ollama request timed out, using original prompt")
        return prompt
    except Exception as e:
        print(f"\n⚠ Warning: Error enhancing prompt ({str(e)}), using original prompt")
        return prompt


def save_prompt_to_file(prompt, filename="prompt.txt"):
    """
    Save the generated prompt to a text file.
    
    Args:
        prompt (str): The prompt to save
        filename (str): The filename to save to (default: prompt.txt)
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(prompt)
    print(f"Prompt saved to {filename}")


def main():
    """Main function to generate, enhance, and save a prompt."""
    # Generate the base prompt
    prompt = generate_prompt()
    print(f"\nOriginal Prompt:\n{prompt}")
    
    # Enhance the prompt using Ollama
    enhanced_prompt = enhance_prompt_with_ollama(prompt)
    
    if enhanced_prompt != prompt:
        print(f"\nEnhanced Prompt:\n{enhanced_prompt}\n")
    else:
        print()  # Just add newline for formatting
    
    # Save the enhanced prompt to file
    save_prompt_to_file(enhanced_prompt)
    return enhanced_prompt


if __name__ == "__main__":
    main()
