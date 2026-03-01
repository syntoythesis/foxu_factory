# Project Overview

Foxu Factory is a web automation tool that generates images of the character Kirsche (an anime fox girl) using the OpenAI chat interface. The project consists of multiple Python scripts that work together to automate prompt generation, web scraping, email verification, and image downloading.

## Main Components

- **foxu_factory.py**: Main automation script using Selenium WebDriver to interact with OpenAI chat
- **prompt_maker.py**: Random prompt generator for creating varied image prompts
- **gmail.py**: Email verification code retrieval via IMAP for authentication

## Quick Start

Generate a random prompt and create an image:
```bash
python prompt_maker.py && python foxu_factory.py --prompt-file prompt.txt
```

Create an image with a specific prompt:
```bash
python foxu_factory.py --prompt "wearing a red dress at the beach"
```

## Project Structure

```
foxu_factory/
├── foxu_factory.py       # Main automation script
├── prompt_maker.py       # Prompt generation script
├── gmail.py              # Email verification helper
├── creds.yaml            # Credentials (not in git)
├── prompt.txt            # Generated prompts
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── images/               # Output directory
    └── YYYYMMDD/         # Dated subdirectories
```

## File-Specific Instructions

This project uses individual instruction files to maintain detailed documentation for each component. When working with specific files, refer to their corresponding instruction files:

- **foxu_factory.py** → [.github/instructions/foxu-factory.instructions.md](.github/instructions/foxu-factory.instructions.md)
  - Main automation script with Selenium WebDriver
  - Authentication, prompt submission, image detection, and download
  
- **gmail.py** → [.github/instructions/gmail.instructions.md](.github/instructions/gmail.instructions.md)
  - IMAP email connection and verification code extraction
  
- **prompt_maker.py** → [.github/instructions/prompt-maker.instructions.md](.github/instructions/prompt-maker.instructions.md)
  - Random prompt generation with predefined elements
  
- **.gitignore, README.md** → [.github/instructions/project-files.instructions.md](.github/instructions/project-files.instructions.md)
  - Project file management guidelines

## Coding Standards

All Python code in this project follows:
- **PEP 8 style guide**: snake_case naming, 4-space indentation
- **Google-style docstrings**: Clear function documentation
- **Error handling**: Informative error messages and graceful fallbacks
- **Type safety**: Consider adding type hints for improved code quality

## Configuration

Credentials should be stored in `creds.yaml`:
```yaml
username: your_email@example.com
password: your_app_password
```

## Dependencies

Install required packages:
```bash
pip install -r requirements.txt
```

Required:
- selenium (WebDriver automation)
- requests (HTTP downloads)
- pyyaml (Config file parsing)