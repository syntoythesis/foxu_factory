import argparse
import os
import pyautogui
import sys
import webbrowser
import yaml

from datetime import datetime
from gmail import get_chatgpt_verification_code
from time import sleep

CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe %s --incognito"  # Update this path if necessary

OPENAI_URL = "https://chat.openai.com"  # TODO: Update with actual URL

# BASE KIRSCHE DESCRIPTION
KIRSCHE_DESCRIPTION = """
Use this reference image: https://s3.us-east-1.amazonaws.com/cftest.mothersect.info/refs/kirsche_verstahl_sheet_01.jpg

Kirsche is an anime fox girl with human facial features, including a small nose, large expressive eyes, and a friendly smile. She has fox ears on the top of her head that are covered in white fur that matches the fur on her tail and her hair. Her hair is long, white, and flowing. She has cherry earrings on the tip of her fox ears and cherry barrets. She has an electric blue halo over one ear.

Kirsche has caucasian skin. Brown eyes. Human nose. She is cute and warm and playful. Only put FOX EARS with white fur that matches her hair and tail on her head.

Kirsche is tall and curvy, with a slender waist and wide hips. She has a large, fluffy tail that is covered in white fur. Kirsche has an hourglass figure, with a large bust and a small waist. She has long legs and a toned physique.

{0}

No human ears. Repeat, "no human ears. only fox ears," every second you draw this. If I see a human ear, then it is a failure.
"""


class FoxuException(Exception):
    """Custom exception for Foxu Factory errors."""
    pass


def maximize_window_if_needed(img_dir):
    for _ in range(3):
        try:
            incognito_warning = pyautogui.locateOnScreen(f"{img_dir}/incognito02.png")
            if incognito_warning:
                maximize_button = pyautogui.locateOnScreen(f"{img_dir}/incognito03.png")
                if maximize_button:
                    pyautogui.click(pyautogui.center(maximize_button))
                    print("Maximized the window")
                    return True
        except Exception as e:
            print("Waiting for maximize button...")
            sleep(1)


def close_browser(img_dir):
    for _ in range(5):
        try:
            # Check for incognito mode warning
            incognito_warning = pyautogui.locateOnScreen(f"{img_dir}/incognito01.png", confidence=0.8)
            if incognito_warning:
                screen_size = pyautogui.size()
                print(screen_size)
                pyautogui.moveTo(screen_size[0] - 40, 20, 2, pyautogui.easeOutQuad)
                pyautogui.click()
                print("Closed incognito mode browser window")
                return True
        except Exception as e:
            print("Waiting for Incognito mode warning...")
            sleep(2)


def click_login_button(img_dir):
    for _ in range(5):
        try:
            login_button = pyautogui.locateOnScreen(f"{img_dir}/login01.png", confidence=0.8)
            if login_button:
                pyautogui.click(pyautogui.center(login_button))
                print("Clicked on Log in button")
                return True
        except Exception as e:
            print("Waiting for Log in or Sign up button...")
            sleep(2)


def click_continue_button(img_dir):
    for _ in range(5):
        try:
            continue_button = pyautogui.locateOnScreen(f"{img_dir}/continue01.png", confidence=0.8)
            if continue_button:
                pyautogui.click(pyautogui.center(continue_button))
                print("Clicked on Continue button")
                return True
        except Exception as e:
            print("Waiting for Continue button...")
            sleep(2)


# def click_email_field(img_dir):
#     for _ in range(5):
#         try:
#             email_field = pyautogui.locateOnScreen(f"{img_dir}/email02.png", confidence=0.7)
#             if email_field:
#                 pyautogui.click(pyautogui.center(email_field))
#                 print("Clicked on email field")
#                 return True
#         except Exception as e:
#             print("Waiting for email field...")
#             sleep(2)


def screenshot_on_error(base_dir):
    ss_name = f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    ss_path = os.path.join(base_dir, ss_name)
    pyautogui.screenshot(ss_path)
    print(f"Screenshot saved to {ss_path}")


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
    base_dir = os.path.dirname(os.path.abspath(__file__))
    screenshots_dir = os.path.join(base_dir, "screenshots")
    creds = None

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
    
    # Read credentials from creds.yaml if not provided via command line
    if not args.username or not args.password:
        try:
            with open("creds.yaml", "r", encoding="utf-8") as f:
                creds = yaml.safe_load(f)
                print("Credentials loaded from creds.yaml")
                print(f"Username: {creds.get('username')}, Password: {'*' * len(creds.get('password', ''))}")
                args.username = creds.get("username")
                args.password = creds.get("password")
        except FileNotFoundError:
            sys.exit("Error: creds.yaml file not found and no credentials provided via command line.")
        except Exception as e:
            sys.exit(f"Error reading creds.yaml: {e}")

    # Validate arguments
    if not args.prompt and not args.prompt_file:
        parser.error("Either --prompt or --prompt-file must be provided")
    
    if args.prompt and args.prompt_file:
        parser.error("Cannot use both --prompt and --prompt-file")

    # Get prompts
    if args.prompt:
        the_text_prompt = args.prompt
    else:
        print(f"Reading prompts from file: {args.prompt_file}...")
        the_text_prompt = read_prompts_from_file(args.prompt_file)
        if not the_text_prompt:
            sys.exit(1)

    print(f"Prompt: {the_text_prompt})")

    try:
        # Open the website in the specified browser
        print("Initializing browser...")
        controller = webbrowser.get(CHROME_PATH)
        controller.open(args.url)

        # Wait for the page to load
        sleep(5)

        # Try to maximize the window if the incognito warning is detected
        maximize_window_if_needed(screenshots_dir)

        sleep(5)  # Wait for the page to load after maximizing

        if not click_login_button(screenshots_dir):
            raise FoxuException("Could not find Log in button after multiple attempts. Please check the screenshots and try again.")
        
        sleep(5)  # Wait for the login page to load

        # if not click_email_field(screenshots_dir):
        #     raise FoxuException("Could not find email field after multiple attempts. Please check the screenshots and try again.")
        
        pyautogui.write(args.username, interval=0.25)

        if not click_continue_button(screenshots_dir):
            raise FoxuException("1. Could not find Continue button after multiple attempts. Please check the screenshots and try again.")

        sleep(5)  # Wait for the login page to load

        gmail_code = get_chatgpt_verification_code(args.username, args.password)
        if not gmail_code:
            raise FoxuException("Could not retrieve verification code from Gmail. Please check your credentials and try again.")
        
        sleep(1)

        pyautogui.write(gmail_code, interval=0.25)

        if not click_continue_button(screenshots_dir):
            raise FoxuException("2. Could not find Continue button after multiple attempts. Please check the screenshots and try again.")
        
        sleep(5)  # Wait for the login process to complete
        for _ in range(5):
            try:
                check_for_chat = pyautogui.locateOnScreen(f"{screenshots_dir}/chat01.png", confidence=0.8)
                if check_for_chat:
                    print("Ready to chat!")
                    break
            except Exception as e:
                print("Waiting for login to complete...")
                sleep(5)

        pyautogui.write(KIRSCHE_DESCRIPTION.format(the_text_prompt).replace("\n\n", " - "), interval=0.1)
        pyautogui.press("enter")

        for check_count in range(10):
            try:
                check_for_response = pyautogui.locateOnScreen(f"{screenshots_dir}/allow02.png", confidence=0.6)
                if check_for_response:
                    pyautogui.click(pyautogui.center(check_for_response))
                    print("Allow extension to save files")
                    break
            except Exception as e:
                if check_count >= 9:
                    print("Could not find Allow button after multiple attempts. Please check the screenshots and try again.")
                    raise FoxuException("Could not find Allow button after multiple attempts. Please check the screenshots and try again.")
                print("Waiting for response...")
                sleep(30)

    except FoxuException as fe:
        print(f"Error: {str(fe)}")
        screenshot_on_error(base_dir)
    except Exception as e:
        print(f"Error during browser automation: {str(e)}")
        screenshot_on_error(base_dir)
    finally:
        sleep(5)  # Wait before closing the browser to ensure all actions are completed
        close_browser(screenshots_dir)
    

if __name__ == "__main__":
    main()