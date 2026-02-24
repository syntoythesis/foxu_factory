#!/usr/bin/env python3
"""
Foxu Factory - OpenAI Chat Image Generator
Automates image generation from OpenAI chat interface using Selenium.
"""

import argparse
import sys
import time
import requests
import subprocess
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from gmail import get_chatgpt_verification_code


# Configuration - UPDATE THESE AFTER INSPECTING THE UI
OPENAI_URL = "https://chat.openai.com"  # TODO: Update with actual URL

# Selectors - UPDATE THESE AFTER INSPECTING THE UI
SELECTORS = {
    "prompt_input": "#prompt-textarea > p",  # TODO: Update selector
    "submit_button": "#composer-submit-button",  # TODO: Update selector
    "generated_image": "//img[@alt='Generated image']",  # TODO: Update selector
    "login_button": "#conversation-header-actions > div > div > button.btn.relative.group-focus-within\/dialog\:focus-visible\:\[outline-width\:1\.5px\].group-focus-within\/dialog\:focus-visible\:\[outline-offset\:2\.5px\].group-focus-within\/dialog\:focus-visible\:\[outline-style\:solid\].group-focus-within\/dialog\:focus-visible\:\[outline-color\:var\(--text-primary\)\].btn-primary",  # TODO: Update selector
    "email_input": "//input[@name='email' and @type='email']",  # TODO: Update selector
    "continue_button": "(//div[contains(@class, 'flex items-center justify-center') and contains(text(), 'Continue')])[last()]",
    "email_code_input": "//input[@type='text' and @name='code']",  # TODO: Update selector
    "email_code_submit": "//button[@type='submit' and @name='intent' and contains(text(), 'Continue')]",  # TODO: Update selector
}

# Wait times (in seconds)
WAIT_TIMEOUT = 300  
POLL_INTERVAL = 10

# BASE KIRSCHE DESCRIPTION
KIRSCHE_DESCRIPTION = """
Kirsche is an anime fox girl with human facial features, including a small nose, large expressive eyes, and a friendly smile. She has fox ears on the top of her head that are covered in white fur that matches the fur on her tail and her hair. Her hair is long, white, and flowing. She has cherry earrings and cherry barrets. She has an electric blue halo over one ear.

Kirsche has caucasian skin. Brown eyes. Human nose. She is cute and warm and playful. Kirsche DOES NOT have human ears. NEVER put human ears on her face. ONLY FOX EARS with white fur that matches her hair and tail.

Kirsche is tall and curvy, with a slender waist and wide hips. She has a large, fluffy tail that is covered in white fur. Kirsche has an hourglass figure, with a large bust and a small waist. She has long legs and a toned physique.

{0}
"""


def setup_driver():
    """Initialize and configure the Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    # Keep browser open for manual authentication
    options.add_experimental_option("detach", True)
    # Run headless - uncomment to enable
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")  # Required on Windows
    # options.add_argument("--no-sandbox")  # Recommended for headless
    # options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


def automated_login(driver, username, password):
    """Perform automated login to OpenAI."""
    print("Starting automated login...")
    
    # Click login button
    print("Looking for login button...")
    login_button = find_element_safe(driver, SELECTORS["login_button"], timeout=5)
    if not login_button:
        print("Login button not found. May already be logged in or page structure changed.")
        return False
    
    login_button.click()
    time.sleep(2)
    
    # Enter email
    print("Entering email...")
    email_input = find_element_safe(driver, SELECTORS["email_input"], by=By.XPATH)
    if not email_input:
        return False
    email_input.clear()
    email_input.send_keys(username)
    time.sleep(2)
    
    # Click continue button
    print("Clicking continue...")
    continue_button = find_element_safe(driver, SELECTORS["continue_button"], by=By.XPATH)
    if not continue_button:
        return False
    continue_button.click()
    time.sleep(10)

    email_code_from_gmail = get_chatgpt_verification_code(username, password)
    if not email_code_from_gmail:
        print("Failed to retrieve verification code from Gmail.")
        return False
    
    # Enter password
    print("Entering password...")
    password_input = find_element_safe(driver, SELECTORS["email_code_input"], by=By.XPATH)
    if not password_input:
        return False
    password_input.clear()
    password_input.send_keys(email_code_from_gmail)
    print("Password entered, waiting before submitting...")
    time.sleep(10)
    
    # Click login submit button
    print("Submitting login...")
    login_submit = find_element_safe(driver, SELECTORS["email_code_submit"], by=By.XPATH)
    if not login_submit:
        return False
    login_submit.click()
    time.sleep(2)
    
    print("Login complete!")
    return True


def wait_for_manual_auth(driver):
    """Wait for user to manually authenticate."""
    print("\n" + "="*50)
    print("MANUAL AUTHENTICATION REQUIRED")
    print("="*50)
    print("Please log in to OpenAI in the browser window.")
    print("Press ENTER here when you're logged in and ready to continue...")
    print("="*50 + "\n")
    input()


def check_login_required(driver):
    """Check if login button is present on the page."""
    try:
        driver.find_element(By.CSS_SELECTOR, SELECTORS["login_button"])
        return True
    except:
        return False


def find_element_safe(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    """Safely find an element with wait and error handling."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        return element
    except TimeoutException:
        print(f"Error: Could not find element with selector: {selector}")
        print("Please update the selector in the script.")
        return None


def submit_prompt(driver, prompt_text):
    """Submit a prompt to the OpenAI chat interface."""
    print(f"Submitting prompt: {prompt_text[:50]}...")
    
    # Find prompt input field
    prompt_input = find_element_safe(driver, SELECTORS["prompt_input"])
    if not prompt_input:
        return False
    
    # Click to focus the input element
    print("Focusing prompt input...")
    prompt_input.click()
    time.sleep(5)
    
    # Enter prompt text
    print("Entering prompt...")
    full_prompt = KIRSCHE_DESCRIPTION.format(prompt_text).replace("\n\n", " - ")
    prompt_input.send_keys(full_prompt)
    time.sleep(10)
    
    # Submit (try button first, then Enter key as fallback)
    print("Submitting...")
    submit_button = find_element_safe(driver, SELECTORS["submit_button"], timeout=10)
    if submit_button:
        submit_button.click()
    else:
        print("Submit button not found, trying Enter key...")
        prompt_input.send_keys(Keys.RETURN)
    
    return True


def wait_for_image_generation(driver, timeout=WAIT_TIMEOUT):
    """Wait for image generation to complete."""
    print("Waiting for image generation...")
    start_time = time.time()
    
    # TODO: Implement proper completion detection
    # For now, we'll use a simple polling approach
    while time.time() - start_time < timeout:
        
        # Check if image element exists
        try:
            image = driver.find_element(By.XPATH, SELECTORS["generated_image"])
            if image and image.get_attribute("src"):
                print("Image detected!")
                time.sleep(2)  # Extra wait to ensure image is fully loaded
                print("Generation complete!")
                print(f"Image URL: {image.get_attribute('src')}")
                return image.get_attribute("src")
        except:
            print(".", end="", flush=True)
            pass
        
        time.sleep(POLL_INTERVAL)
        print(".", end="", flush=True)
    
    print("\nTimeout waiting for image generation.")
    return False


def download_image(driver, output_path):
    """Download the generated image."""
    print(f"Downloading image to: {output_path}")
    time.sleep(10)  # Ensure image is fully loaded
    
    # Find the image element
    try:
        image = driver.find_element(By.XPATH, SELECTORS["generated_image"])
        image_url = image.get_attribute("src")
        
        if not image_url:
            print("Error: Image element found but no src attribute.")
            return False
        
        # Handle data URLs or remote URLs
        if image_url.startswith("data:"):
            print("Error: Data URL detected. Need to implement data URL handling.")
            print("Please right-click the image and 'Save image as...' manually for now.")
            return False
        
        # Get cookies from Selenium to maintain session
        cookies = driver.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        # Download the image
        response = session.get(image_url, stream=True)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Image saved successfully: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False


def create_output_directory():
    """Create dated output directory (images/YYYYMMDD/)."""
    date_str = datetime.now().strftime("%Y%m%d")
    output_dir = Path("images") / date_str
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def process_prompt(driver, prompt_text, output_filename):
    """Process a single prompt: submit, wait, and download."""
    # Create output directory
    output_dir = create_output_directory()
    output_path = output_dir / output_filename
    
    # Submit prompt
    if not submit_prompt(driver, prompt_text):
        return False
    
    # Wait for generation
    if not wait_for_image_generation(driver):
        return False
    
    # Download image
    return download_image(driver, output_path)


def read_prompts_from_file(prompt_file):
    """Read prompts from a text file (one per line)."""
    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt = " - ".join([line.strip() for line in f if line.strip()])
        return prompt
    except Exception as e:
        print(f"Error reading prompt file: {e}")
        return None


def main():
    """Main entry point for the screen crawler."""
    parser = argparse.ArgumentParser(
        description="Automate image generation from OpenAI chat interface"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="Single prompt text for image generation"
    )
    parser.add_argument(
        "--prompt-file",
        type=str,
        help="File containing prompts (one per line)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output filename (e.g., 'cat.png')"
    )
    parser.add_argument(
        "--url",
        type=str,
        default=OPENAI_URL,
        help=f"OpenAI chat URL (default: {OPENAI_URL})"
    )
    parser.add_argument(
        "--username",
        type=str,
        help="Username/email for automated login (optional)"
    )
    parser.add_argument(
        "--password",
        type=str,
        help="Password for automated login (optional)"
    )
    
    args = parser.parse_args()
    
    # Validate username/password pairing
    if (args.username and not args.password) or (args.password and not args.username):
        parser.error("Both --username and --password must be provided together")
    
    # Validate arguments
    if not args.prompt and not args.prompt_file:
        parser.error("Either --prompt or --prompt-file must be provided")
    
    if args.prompt and args.prompt_file:
        parser.error("Cannot use both --prompt and --prompt-file")

    output_filename = args.output if args.output else f"output_{uuid4().hex[:8]}.png"
    
    # Get prompts
    if args.prompt:
        the_text_prompt = args.prompt
    else:
        print(f"Reading prompts from file: {args.prompt_file}...")
        the_text_prompt = read_prompts_from_file(args.prompt_file)
        if not the_text_prompt:
            sys.exit(1)

    print(f"Prompt: {the_text_prompt})")
    
    # Setup driver
    print("Initializing browser...")
    driver = setup_driver()
    
    try:
        # Navigate to OpenAI
        print(f"Navigating to {args.url}...")
        driver.get(args.url)
        time.sleep(2)  # Wait for page load
        
        # Handle authentication
        if args.username and args.password:
            # Automated login
            if not automated_login(driver, args.username, args.password):
                print("Automated login failed. Please log in manually.")
                wait_for_manual_auth(driver)
        else:
            # Check if login is required
            if check_login_required(driver):
                print("Login detected. No credentials provided.")
                wait_for_manual_auth(driver)
            else:
                print("No login required or already logged in.")
        
        success = process_prompt(
            driver, the_text_prompt, output_filename)
        
        if not success:
            print(f"Failed to process prompt....")
            # Continue with next prompt or exit?
        
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # print("\nKeeping browser open for inspection...")
        # print("Close the browser window manually when done.")
        print("\nExiting script.")
        time.sleep(10)
        driver.quit()


if __name__ == "__main__":
    main()
