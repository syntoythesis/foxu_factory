# Foxu Factory

## Description

A web crawler/scraper that automates image generation from OpenAI chat interface using Selenium. The app submits image prompts to the OpenAI chat interface, waits for image generation, and downloads the resulting images to dated directories. Built with Python and Selenium Chrome WebDriver, it supports both single prompts and batch processing from files, with automated or manual authentication options.

## Update Log

**2026-02-24**: Created comprehensive `foxu-factory.instructions.md` documentation file with detailed workflow, architecture, and maintenance notes. Restructured `copilot-instructions.md` to serve as project overview that delegates to individual instruction files for each component. Updated `.gitignore` and `README.md` to follow project file guidelines.

**2026-02-24**: Added `prompt_maker.py` to generate random prompts for Kirsche images based on predefined templates and elements. Updated README with instructions for using the prompt generator.

**2026-02-23**: Added instructions for Gmail verification code retrieval using IMAP in `gmail.py`, because OpenAI now requires email verification for login. Updated `foxu_factory.py` to integrate Gmail code retrieval for authentication.

**2026-02-22**: Updated copilot instructions to match actual implementation in foxy_factory.py. Created .gitignore and restructured README to follow project guidelines.
