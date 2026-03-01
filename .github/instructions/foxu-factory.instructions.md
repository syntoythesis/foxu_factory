---
applyTo: 'foxu_factory.py'
description: 'This script automates image generation from the OpenAI chat interface using Selenium WebDriver.'
---

# About

Foxu Factory is a web automation script that uses Selenium with Chrome WebDriver to interact with the OpenAI chat interface. It submits image generation prompts, waits for images to be created, and automatically downloads the generated images.

The script is designed to generate images of a character named Kirsche (an anime fox girl) by prepending a detailed character description to user prompts. It handles authentication, prompt submission, image detection, and download operations automatically.

## Command Line Usage

Basic usage with a text prompt:
```bash
python foxu_factory.py --prompt "a cat sitting on a windowsill" --output "cat.png"
```

Using a prompt file (joins lines with " - " separator):
```bash
python foxu_factory.py --prompt-file "prompt.txt" --output "cat.png"
```

## Command Line Parameters

**Required (one of):**
- `--prompt`: Single prompt text for image generation
- `--prompt-file`: File containing prompts (one per line, joined with " - ")

**Optional:**
- `--username`: Username/email for automated login (must be paired with --password)
- `--password`: Password for automated login (must be paired with --username)
- `--url`: The URL of the OpenAI chat app (default: https://chat.openai.com/)
- `--output`: Output filename (default: generates filename like `output_XXXXXXXX.png` with random UUID)

**Credentials File:**
If credentials are not provided via command line, the script will attempt to load them from `creds.yaml` in the root directory with the following format:
```yaml
username: your_email@example.com
password: your_password
```

## Output Structure

Images are automatically saved to dated directories:
```
images/
  YYYYMMDD/
    output_XXXXXXXX.png
    custom_name.png
```

# Architecture

## Key Components

1. **WebDriver Setup** (`setup_driver()`): Initializes Chrome WebDriver with options
2. **Authentication** (`automated_login()`, `wait_for_manual_auth()`, `check_login_required()`): Handles login flow
3. **Prompt Processing** (`process_prompt()`): Orchestrates the full workflow for a single prompt
4. **Prompt Submission** (`submit_prompt()`): Enters and submits prompts to the chat interface
5. **Image Detection** (`wait_for_image_generation()`): Polls for generated images
6. **Image Download** (`download_image()`): Downloads images maintaining session cookies
7. **File Management** (`create_output_directory()`, `read_prompts_from_file()`): Handles file operations

## Workflow Function

The `process_prompt()` function orchestrates the complete workflow for a single prompt:
1. Creates output directory using `create_output_directory()`
2. Constructs full output path
3. Calls `submit_prompt()` to submit the prompt
4. If submission fails, returns False
5. Calls `wait_for_image_generation()` to wait for the image
6. If generation fails/times out, returns False
7. Waits an additional 30 seconds for stability
8. Calls `download_image()` to download the generated image
9. Returns the success status of the download

This function is called from `main()` after authentication is complete.

## Configuration

### Selectors
The script uses CSS selectors and XPath expressions to locate elements on the page. These are defined in the `SELECTORS` dictionary and must be updated if the OpenAI UI changes:

```python
SELECTORS = {
    "prompt_input": "#prompt-textarea > p",
    "submit_button": "#composer-submit-button",
    "generating_image": "//span[contains(text(), 'Creating image')]",
    "generated_image": "//img[@alt='Generated image']",
    "login_button": "#conversation-header-actions > div > div > button.btn.relative.group-focus-within\/dialog\:focus-visible\:\[outline-width\:1\.5px\].group-focus-within\/dialog\:focus-visible\:\[outline-offset\:2\.5px\].group-focus-within\/dialog\:focus-visible\:\[outline-style\:solid\].group-focus-within\/dialog\:focus-visible\:\[outline-color\:var\(--text-primary\)\].btn-primary",
    "email_input": "//input[@name='email' and @type='email']",
    "continue_button": "(//div[contains(@class, 'flex items-center justify-center') and contains(text(), 'Continue')])[last()]",
    "email_code_option_link": "//a[contains(text(), 'email') or contains(text(), 'Email') or contains(@href, 'email')]",
    "email_code_input": "//input[@type='text' and @name='code']",
    "email_code_submit": "//button[@type='submit' and @name='intent' and contains(text(), 'Continue')]",
}
```

### Wait Times
```python
WAIT_TIMEOUT = 600  # Maximum time to wait for image generation (seconds)
POLL_INTERVAL = 10  # Time between polling attempts (seconds)
```

### Character Description
The script prepends a detailed description of Kirsche to all prompts. This is stored in the `KIRSCHE_DESCRIPTION` constant and includes:
- Physical appearance (fox ears, white hair, tail)
- Facial features (brown eyes, human nose, large expressive eyes, friendly smile)
- Body type (tall, curvy, hourglass figure)
- Accessories (cherry earrings, cherry barrets, electric blue halo)
- Reference image URL

The final prompt format is: `KIRSCHE_DESCRIPTION.format(user_prompt)`

# Workflow

## 1. Initialization
- Parse command line arguments
- Validate username/password pairing
- Load credentials from `creds.yaml` if not provided via CLI:
  - If file not found, exit with error message
  - If any other error occurs, exit with error message
  - On success, print "Credentials loaded from creds.yaml"
  - Print username and masked password for verification
- Validate prompt source (--prompt or --prompt-file)
- Validate that only one prompt source is provided
- Generate output filename if not provided (format: `output_XXXXXXXX.png` with 8-character UUID)
- Read prompt text from file using `read_prompts_from_file()` if using --prompt-file
- Print the prompt text that will be used
- Setup Chrome WebDriver with options:
  - `detach=True`: Keeps browser open after script ends (note: browser is closed in cleanup)
  - `excludeSwitches=["enable-automation"]`: Hides automation indicators
  - `--disable-gpu`: Required on Windows
  - Commented options available: `--headless`, `--no-sandbox`, `--disable-dev-shm-usage`
- Maximize browser window

## 2. Navigation
- Navigate to OpenAI chat URL (default: https://chat.openai.com/)
- Wait 2 seconds for initial page load

## 3. Authentication

### Automated Login (if credentials provided):
1. Look for login button (5 second timeout)
2. If not found, assume already logged in and continue
3. If found, click login button, wait 2 seconds
4. Enter email in email input field, wait 2 seconds
5. Click continue button, wait 10 seconds
6. Check for email code option link (5 second timeout) - this handles cases where OpenAI shows a password field with a link to use email verification instead
7. If email code option link is found, click it and wait 5 seconds
8. If not found, assume email code field is already displayed and continue
9. Call `get_chatgpt_verification_code()` from gmail.py to retrieve email verification code
10. If code retrieval fails, return False and fall back to manual auth
11. Enter verification code in email code input field, wait 10 seconds
12. Click email code submit button, wait 2 seconds
13. If any step fails, fall back to manual authentication

### Manual Authentication (fallback or no credentials):
1. Check if login button is present on the page
2. If found, display prompt to user:
   ```
   ==================================================
   MANUAL AUTHENTICATION REQUIRED
   ==================================================
   Please log in to OpenAI in the browser window.
   Press ENTER here when you're logged in and ready to continue...
   ==================================================
   ```
3. Wait for user to press ENTER
4. If not found, assume user is already logged in and continue

## 4. Prompt Processing

After authentication completes, `main()` calls `process_prompt(driver, the_text_prompt, output_filename)` which orchestrates the remaining workflow steps (described in sections 4-7).

### Prompt Input (within `submit_prompt()`):
1. Find prompt input element using CSS selector
2. If found, refresh page to ensure clean state, wait 10 seconds
3. Re-find prompt input after refresh
4. Click to focus the input field, wait 5 seconds
5. Construct full prompt by formatting `KIRSCHE_DESCRIPTION` with user's prompt text
6. Replace double newlines with " - " in the full prompt
7. Enter the full prompt text, wait 10 seconds

Note: There is a commented-out line `# full_prompt = prompt_text` that can be uncommented to bypass the Kirsche description prefix and use only the user's prompt text.
6. Enter the full prompt text, wait 10 seconds

### Prompt Submission:
1. Send RETURN key to input field to submit the prompt

## 5. Image Generation Wait

The script polls for image generation completion:

1. Start timer for timeout tracking
2. Initialize refresh counter (`counter_until_refresh = 0`)
3. Loop until timeout (`WAIT_TIMEOUT` = 600 seconds):
   - Check for "Creating image" indicator
     - If found:
       - Print "Still generating image..." message
       - Increment refresh counter
       - If counter > 7, refresh the page (handles stuck UI) and reset counter to 0
       - Wait 30 seconds (longer wait during generation) for each check to reduce polling frequency
       - Continue to next iteration
   - After generation indicator disappears, check for generated image element
   - Try to find generated image element using XPath
   - If found and has `src` attribute:
     - Print "Image detected!" message
     - Wait additional 30 seconds for full load
     - Print "Generation complete!" message
     - Print image URL
     - Return the image URL
   - If not found, wait `POLL_INTERVAL` (10 seconds)
   - Print progress dots to console
4. If timeout reached, print timeout message and return False

## 6. Image Download

Called by `process_prompt()` after a 30-second wait following successful image generation.

1. Wait 10 seconds to ensure image is fully loaded
2. Find image element using XPath
3. Extract `src` attribute (image URL)
4. Handle different URL types:
   - **Data URLs** (`data:...`): Not currently supported, prompt user to save manually
   - **Remote URLs**: Continue with download process
5. Create `requests.Session` and copy all cookies from Selenium to maintain authentication
6. Download image with streaming (`stream=True`)
7. Write image to file in chunks (8192 bytes)
8. Save to dated output directory: `images/YYYYMMDD/filename.png`
9. Print success message with file path

## 7. Output Directory Structure

The `create_output_directory()` function:
1. Gets current date in `YYYYMMDD` format
2. Creates directory path: `images/YYYYMMDD/`
3. Creates directory with `parents=True` and `exist_ok=True`
4. Returns the Path object

## 8. Cleanup

In the `finally` block:
1. Print "Exiting script." message
2. Wait 5 seconds
3. Call `driver.quit()` to close browser and clean up WebDriver

Note: Earlier versions kept the browser open for inspection. The current version automatically closes the browser.

# Error Handling

## Element Finding
The `find_element_safe()` helper function:
- Uses `WebDriverWait` with configurable timeout
- Catches `TimeoutException`
- Prints helpful error messages with selector information
- Returns `None` on failure (allows script to continue or handle gracefully)

## Authentication Failures
- Automated login returns `False` on any step failure
- Falls back to manual authentication prompt
- User can manually log in and continue

## Download Failures
- Logs error messages for:
  - Missing image element
  - Missing `src` attribute
  - Data URLs (not yet supported)
  - Network errors during download
  - File write errors

## Keyboard Interrupt
- Catches `KeyboardInterrupt` (Ctrl+C)
- Prints "Interrupted by user."
- Proceeds to cleanup in `finally` block

## General Exceptions
- Catches all other exceptions in the main try block
- Prints error message with exception details
- Prints full traceback using `traceback.print_exc()`
- Proceeds to cleanup in `finally` block

# Dependencies

Required Python packages (from requirements.txt):
- `selenium`: Web automation framework
- `requests`: HTTP library for image downloads
- `pyyaml`: YAML file parsing for credentials

External dependencies:
- Chrome browser
- ChromeDriver (managed by selenium-manager in Selenium 4+)

Custom modules:
- `gmail.py`: Provides `get_chatgpt_verification_code()` function for email verification

# Integration with Other Scripts

## gmail.py
The script imports and uses `get_chatgpt_verification_code(username, password)` to:
- Connect to Gmail via IMAP
- Retrieve the most recent verification code email from OpenAI
- Extract and return the verification code

## prompt_maker.py
While not directly imported, the workflow supports:
- Running `prompt_maker.py` to generate `prompt.txt`
- Using `--prompt-file prompt.txt` to submit generated prompts

Example:
```bash
python prompt_maker.py && python foxu_factory.py --prompt-file prompt.txt
```

# Coding Conventions

- **Style**: PEP 8 compliant
  - snake_case for functions and variables
  - UPPER_CASE for constants
  - 4 spaces for indentation
- **Type hints**: Not used (could be added for improved type safety)
- **Docstrings**: Google-style docstrings for all functions
- **Error handling**: Try/except blocks with informative error messages
- **Logging**: Print statements for user feedback and debugging

# Maintenance Notes

## Updating Selectors
If the OpenAI UI changes, update the `SELECTORS` dictionary:
1. Open browser DevTools (F12)
2. Use "Select Element" tool to inspect target elements
3. Copy CSS selector or create XPath expression
4. Test selectors in browser console before updating script
5. Update corresponding entry in `SELECTORS` dictionary

## Adjusting Wait Times
If generation is slower or faster:
- Increase/decrease `WAIT_TIMEOUT` for overall timeout
- Adjust `POLL_INTERVAL` for polling frequency
- Modify hardcoded `time.sleep()` calls in critical sections

## Character Description
To use for different characters:
- Modify `KIRSCHE_DESCRIPTION` constant
- Update reference image URL
- Adjust formatting in `submit_prompt()` if needed
