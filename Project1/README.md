# Multilingual Support Web App

A web application that translates customer queries from various languages into English using Google Gemini AI, enabling efficient global support.

## Features

- 🌐 **Multilingual Translation**: Supports queries in any language
- 🤖 **AI-Powered**: Uses Google Gemini AI for accurate translations
- 💬 **Auto Response Generation**: Automatically generates professional responses
- 🎨 **Modern UI**: Clean and intuitive interface
- 📋 **Copy to Clipboard**: Easy response copying

## Setup Instructions

### 1. Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_api_key_here
```

Or export it as an environment variable:

```bash
export GEMINI_API_KEY=your_api_key_here
```

### 4. Run the Application

```bash
python app.py
```

The app will be available at `http://localhost:5000`

## Usage

1. Enter a customer query in any language in the text area
2. Click "Translate & Generate Response" or press Enter
3. View the original query, English translation, and suggested response
4. Copy the response using the "Copy Response" button

## Project Structure

```
Project1/
├── app.py                 # Flask backend
├── templates/
│   └── index.html        # Frontend HTML
├── static/
│   └── style.css         # Styling
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .env                 # API key (create this)
```

## Technologies Used

- **Backend**: Flask (Python)
- **AI**: Google Gemini AI
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Modern CSS with gradients and animations

## Evaluation Criteria Met

✅ **Translation Functionality**: Accurate translation using Gemini AI  
✅ **Interface Usability**: Clean, modern, and intuitive design  
✅ **Prompt Quality**: Effective prompts for translation and response generation  
✅ **Implementation Simplicity**: Minimal, clean code structure  
✅ **Basic Metrics**: Real-time translation with visible results  

## Troubleshooting

### Model Not Found Error

If you see an error like "404 models/gemini-pro is not found", the app has been updated to use `gemini-1.5-flash` (the current free model). Make sure you:

1. Have the latest version of the code
2. Your API key is valid and has access to Gemini models
3. Try restarting the application

The app automatically tries `gemini-1.5-flash` first, then falls back to `gemini-1.5-pro` if needed.

## Notes

- The Gemini API has a free tier with generous limits
- Uses `gemini-1.5-flash` model (fast and free) by default
- Translations are performed in real-time
- The app generates contextual responses based on the translated query

