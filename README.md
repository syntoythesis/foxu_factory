# Foxu Factory

## Description

A web crawler/scraper that automates image generation from OpenAI chat interface using Selenium. The app submits image prompts to the OpenAI chat interface, waits for image generation, and downloads the resulting images to dated directories. Built with Python and Selenium Chrome WebDriver, it supports both single prompts and batch processing from files, with automated or manual authentication options.

## Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Update `creds.yaml` with your GMail email and [app password](https://support.google.com/accounts/answer/185833?hl=en).
3. Run the script: `python foxu_factory.py`
4. Fix whatever breaks because OpenAI keeps changing their login flow and UI.

## To Do

1. Run headless and deploy to a server.
2. Use AI to look at the page befrore deciding how to interact with it, to make the bot more resilient to UI changes.

## Update Log

**2026-02-23**: Added instructions for Gmail verification code retrieval using IMAP in `gmail.py`, because OpenAI now requires email verification for login. Updated `foxu_factory.py` to integrate Gmail code retrieval for authentication.
**2026-02-22**: Updated copilot instructions to match actual implementation in foxy_factory.py. Created .gitignore and restructured README to follow project guidelines.
