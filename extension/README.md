# Foxu Factory Chrome Extension

Automatically downloads generated images from ChatGPT.

## Features

- Monitors chat.openai.com and chatgpt.com for "IMAGE CREATED" text every 30 seconds (case-insensitive)
- Searches within the `main` tag for better accuracy
- Automatically downloads generated images when detected using Chrome downloads API
- Sends image URL to local server at http://localhost:8787/image
- No configuration needed - works out of the box
- Downloads to your default Chrome download folder
- Works in Incognito mode

## Installation

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" using the toggle in the top right corner
3. Click "Load unpacked"
4. Select the `extension` folder from this project
5. The extension is now installed and active

## Usage

1. Navigate to chat.openai.com or chatgpt.com
2. Generate an image using ChatGPT
3. When the page shows "Image Created", the extension will automatically detect and download the generated image
4. Check your Downloads folder for the saved image (filename format: `foxu-YYYY-MM-DDTHH-MM-SS-mmmZ.png`)

## How It Works

- Content script runs on ChatGPT pages and localhost:8787
- Checks every 30 seconds for "IMAGE CREATED" text within the `main` tag (case-insensitive)
- Searches for images within `main` tag with:
  - `alt="Generated image"` OR
  - `src` starting with `https://chatgpt.com/backend-api/estuary/content`
- Automatically triggers download via Chrome's downloads API through background service worker
- Sends POST request with image URL to http://localhost:8787/image
- Logs image URLs to browser console for debugging
- Prevents duplicate downloads by tracking processed images

## Files with download permissions for Incognito mode
- `content.js` - Content script that detects images and sends to background worker
- `background.js` - Service worker that handles downloads using Chrome downloads API
- `content.js` - Content script that detects images on the page
- `background.js` - Service worker that handles downloads

## Troubleshooting

- Open browser console (F12) to see debug messages
- Check if "Image Created" text appears on the page
- Verify the extension is enabled in chrome://extensions/
- Ensure you're on chat.openai.com or chatgpt.com (not subdomains)
