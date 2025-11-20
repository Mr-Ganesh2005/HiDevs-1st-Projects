from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini AI
api_key = os.getenv('GEMINI_API_KEY')
model = None
model_name = None

if api_key:
    genai.configure(api_key=api_key)
    # List available models and find one that supports generateContent
    try:
        available_models = list(genai.list_models())
        print("\n=== Available Models ===")
        suitable_models = []
        
        for m in available_models:
            methods = getattr(m, 'supported_generation_methods', [])
            name = getattr(m, 'name', '')
            # Clean model name (remove 'models/' prefix if present)
            clean_name = name.replace('models/', '') if name.startswith('models/') else name
            
            if 'generateContent' in methods:
                suitable_models.append(clean_name)
                print(f"  ✓ {clean_name} (supports generateContent)")
            else:
                print(f"  ✗ {clean_name} (does not support generateContent)")
        
        # Prefer flash models (faster, free tier), then pro models
        preferred_order = [
            'gemini-1.5-flash',
            'gemini-1.5-flash-latest',
            'gemini-1.5-pro',
            'gemini-1.5-pro-latest',
            'gemini-pro',
            'gemini-pro-latest'
        ]
        
        # Find first available model in preferred order
        for preferred in preferred_order:
            if preferred in suitable_models:
                model_name = preferred
                break
        
        # If no preferred model found, use first suitable model
        if not model_name and suitable_models:
            model_name = suitable_models[0]
        
        if model_name:
            model = genai.GenerativeModel(model_name)
            print(f"\n✓ Successfully initialized model: {model_name}\n")
        else:
            print("\n✗ Error: No suitable model found that supports generateContent")
            print("Please check your API key permissions.\n")
            model = None
            
    except Exception as e:
        print(f"\n✗ Error listing models: {e}")
        print("Attempting fallback to common model names...\n")
        # Last resort: try common model names directly
        for name in ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']:
            try:
                model = genai.GenerativeModel(name)
                model_name = name
                print(f"✓ Using model: {model_name}\n")
                break
            except Exception as fallback_error:
                print(f"  ✗ {name}: {fallback_error}")
                continue
        if not model:
            print("✗ Could not initialize any model. Please check your API key.\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debug/models', methods=['GET'])
def debug_models():
    """Debug endpoint to list available models"""
    if not api_key:
        return jsonify({'error': 'API key not configured'}), 500
    
    try:
        available_models = list(genai.list_models())
        models_info = []
        for m in available_models:
            methods = getattr(m, 'supported_generation_methods', [])
            name = getattr(m, 'name', '')
            clean_name = name.replace('models/', '') if name.startswith('models/') else name
            models_info.append({
                'name': clean_name,
                'full_name': name,
                'supports_generateContent': 'generateContent' in methods,
                'methods': list(methods) if methods else []
            })
        return jsonify({
            'success': True,
            'current_model': model_name,
            'models': models_info
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Please enter a query'}), 400
        
        if not model:
            return jsonify({'error': 'Gemini API key not configured. Please set GEMINI_API_KEY in your environment.'}), 500
        
        # Create a prompt for translation
        prompt = f"""Translate the following customer query to English. 
        If the query is already in English, return it as is.
        Only provide the English translation, nothing else.
        
        Query: {query}
        
        English Translation:"""
        
        # Get translation from Gemini
        response = model.generate_content(prompt)
        translated_text = response.text.strip()
        
        # Optional: Generate a predefined response
        response_prompt = f"""Based on this customer query in English: "{translated_text}"
        
        Generate a brief, helpful, and professional response. Keep it concise (2-3 sentences max).
        Response:"""
        
        ai_response = model.generate_content(response_prompt)
        generated_response = ai_response.text.strip()
        
        return jsonify({
            'success': True,
            'original': query,
            'translated': translated_text,
            'response': generated_response
        })
        
    except Exception as e:
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

