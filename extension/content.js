// Track already downloaded images to avoid duplicates
const downloadedImages = new Set();

// Check for generated images every 30 seconds
setInterval(() => {
  checkForGeneratedImage();
}, 30000);

// Also check immediately on load
setTimeout(() => {
  checkForGeneratedImage();
}, 2000);

function checkForGeneratedImage() {
  // Check if "Image Created" text is present within the main tag
  const mainElement = document.querySelector('main');
  if (!mainElement) {
    return;
  }
  
  const mainText = mainElement.innerText;
  if (!mainText.toUpperCase().includes('IMAGE CREATED')) {
    return;
  }

  // Find image with alt="Generated image" or src starting with the specific URL within main tag
  const images = mainElement.querySelectorAll('img');
  
  for (const img of images) {
    const alt = img.getAttribute('alt');
    const src = img.getAttribute('src');
    
    if (alt === 'Generated image' || 
        (src && src.startsWith('https://chatgpt.com/backend-api/estuary/content'))) {
      
      // Skip if already downloaded
      if (downloadedImages.has(src)) {
        continue;
      }
      
      console.log(src);
      
      // Mark as downloaded and trigger download
      downloadedImages.add(src);
      downloadImage(src);
      
      // Send POST request to localhost server
      sendToServer(src);
      
      // Only download the first new match
      break;
    }
  }
}

function downloadImage(url) {
  if (!url) return;
  
  // Send message to background script to download using Chrome downloads API
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `foxu-${timestamp}.png`;
  
  chrome.runtime.sendMessage({
    action: 'download',
    url: url,
    filename: filename
  });
}

function sendToServer(url) {
  if (!url) return;
  
  fetch('http://localhost:8787/image', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url: url })
  })
  .then(response => {
    if (response.ok) {
      console.log('Image URL sent to server successfully');
    } else {
      console.error('Failed to send image URL to server:', response.statusText);
    }
  })
  .catch(error => {
    console.error('Error sending image URL to server:', error);
  });
}
