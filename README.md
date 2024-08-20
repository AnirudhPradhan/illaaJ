# illaaJ - The AI Doctor Assistant

![Project Logo](link-to-your-logo.png)

illaaJ is an AI-powered doctor assistant that helps you detect diseases based on your symptoms and provides home remedies. With a simple and intuitive interface, illaaJ aims to offer quick and accessible healthcare solutions to everyone.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features
- **Symptom Detection:** Enter your symptoms, and illaaJ will provide a list of potential diseases.
- **Home Remedies:** Get tailored remedies that you can easily take at home to alleviate your symptoms.
- **User-Friendly Interface:** Simple design with easy navigation to ensure a seamless user experience.
- **Fast and Accurate:** Leveraging AI to quickly provide accurate diagnostic results.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/illaaJ.git
   cd illaaJ
Made with
Tech used	For
React.js	Frontend
Flask	Backend
MongoDB	Database
Tensorflow and CustomVision	ML model to detect ingredients in picture
SciKit Learn	ML model to find matching recipes
Google Cloud	Hosting
Cloudflare	CDN for static data
Setup process
Frontend
Open frontend/src/index.js and update window.APIROOT to the base URL for the backend. Default URL is given below.
window.APIROOT = "http://127.0.0.1:4950/"
Run the below command in frontend folder.
npm install
Backend
Run the below command in backend folder.
pip install -r requirements.txt
Create an OAuth client ID in Google cloud console with the below info.
# Authorized JavaScript origins

http://127.0.0.1:4950
https://127.0.0.1:4950

# Authorized redirect URIs

http://127.0.0.1:4950/callback
https://127.0.0.1:4950/callback
Download the client_secret.json file and save it in the backend folder.

Create a YouTube Data API v3 key from Google cloud console.

Include an attribute data in the client_secret.json file as below.

{
  "web": {
    // No changes here
  },
  "data": {
    "redirect_uri": "http://127.0.0.1:4950/callback",
    "home": "http://127.0.0.1:3000",
    "mongo": "MongoDB URL here",
    "youtube": "YouTube Data API v3 key here"
  }
}
Running process
Frontend
Run the below command in the frontend folder.

npm run start
Backend
Run the below command in the backend folder.

python main.py
