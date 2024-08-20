from flask import Flask, render_template, request
import google.generativeai as genai
import json
import re
import os

# Retrieve the API key from environment variables
api_key = os.getenv("api_key")
if not api_key:
    raise ValueError("No API key found in environment variables.")

# Configure the Gemini API with the retrieved API key
genai.configure(api_key=api_key)

app = Flask(__name__)

def load_database():
    """Load the disease dataset from a JSON file."""
    try:
        with open('database/disease_dataset.json') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def diagnose(symptoms):
    """Diagnose diseases based on the provided symptoms."""
    database = load_database()
    matched_diseases = []
    symptoms_set = {symptom.lower() for symptom in symptoms}  # Convert symptoms to lowercase

    for entry in database:
        disease_symptoms = {symptom.lower() for symptom in entry["Symptom"]}  # Convert symptoms in the database to lowercase
        if symptoms_set.issubset(disease_symptoms):
            matched_diseases.append(entry["Disease"])

    return matched_diseases

def get_remedies(disease):
    """Fetch and format remedies for a given disease using the Gemini API."""
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        prompt = f'''You are my assistance. Fetch the precautions for {disease} and provide in brief and return in dot points.
        In format - {disease}:
        1. Precaution 1
        2. Precaution 2.. etc
        At least write 10 precautions.
        '''
        response = model.generate_content(prompt)
        text = response.to_dict()['candidates'][0]['content']['parts'][0]['text']
        text = format_bullet_points(text)
        return text
    except Exception as e:
        return f"Error: {str(e)}"

def format_bullet_points(text):
    """Format the text into an HTML unordered list."""
    # Remove Markdown headings (e.g., ## Mumps)
    text = re.sub(r'^##\s+', '', text, flags=re.MULTILINE)
    
    # Define the regex pattern for bullet points followed by text
    pattern = r'(\d+\.\s)\*\*(.*?)\*\*(.*?)(?=\d+\.\s|$)'

    # Replace matched pattern with HTML formatting
    formatted_text = re.sub(pattern, r'<li><strong>\2</strong>\3</li>\n', text, flags=re.DOTALL)

    # Wrap in <ul> tags to create an unordered list
    formatted_text = f"<ul>{formatted_text}</ul>"
    
    return formatted_text.strip()

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/diagnose', methods=['GET', 'POST'])
def diagnose_route():
    """Handle the diagnosis route."""
    diseases = None
    if request.method == 'POST':
        symptoms_input = request.form.get('Symptom')
        if symptoms_input:
            symptoms_list = [symptom.strip().lower() for symptom in symptoms_input.split(',')]  # Convert input to lowercase
            diseases = diagnose(symptoms_list)
    return render_template('diagnose.html', diseases=diseases)

@app.route('/remedies', methods=['GET', 'POST'])
def remedies_route():
    """Handle the remedies route."""
    selected_disease = None
    remedies = None
    if request.method == 'POST':
        selected_disease = request.form.get('Disease')
        if selected_disease:
            remedies = get_remedies(selected_disease)
    return render_template('remedies.html', selected_disease=selected_disease, remedies=remedies)

if __name__ == '__main__':
    app.run(debug=True)
