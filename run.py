from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
import json
import re
from secure import key

# Configure the Gemini API
genai.configure(api_key=key)

app = Flask(__name__)

def load_database():
    try:
        with open('database/disease_dataset.json') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def diagnose(symptoms):
    database = load_database()
    matched_diseases = []
    symptoms_set = set(symptoms)

    for entry in database:
        disease_symptoms = set(entry["Symptom"])
        if symptoms_set.issubset(disease_symptoms):
            matched_diseases.append(entry["Disease"])

    return matched_diseases

def get_remedies(disease):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        prompt = f'''You are my assistance. Fetch the precautions for {disease} and provide in brief and return in dot points.
        In format - {disease}:
        1. Precaution 1
        2. Precaution 2.. etc
        atleast write 10 precautions.
        '''
        response = model.generate_content(prompt)
        # print(response)
        response = response.to_dict()
        text = response['candidates'][0]['content']['parts'][0]['text']
        text = format_bullet_points(text)
        return text
    except Exception as e:
        return f"Error: {str(e)}"


def format_bullet_points(text):
    # Define the regex pattern for bullet points followed by text
    # Assuming bullet points are in the format of 1. **bold text** additional text
    pattern = r'(\d+\.\s)\*\*(.*?)\*\*(.*?)(?=\d+\.\s|$)'

    # Replace matched pattern with HTML formatting
    formatted_text = re.sub(pattern, r'<li><strong>\2</strong>\3</li>', text, flags=re.DOTALL)

    # Wrap in <ul> tags to create an unordered list
    formatted_text = f"<ul>{formatted_text}</ul>"
    
    return formatted_text.strip()

@app.route('/', methods=['GET'])
@app.route("/index", methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/diagnose', methods=['GET','POST'])
def diagnose_route():
    diseases = None
    if request.method == 'POST':
        symptoms_input = request.form.get('Symptom')
        if symptoms_input:
            symptoms_list = [symptom.strip() for symptom in symptoms_input.split(',')]
            diseases = diagnose(symptoms_list)
    return render_template('diagnose.html', diseases=diseases)

@app.route('/remedies', methods=['GET','POST'])
def remedies_route():
    selected_disease = None
    remedies = None
    if request.method == 'POST':
        selected_disease = request.form.get('Disease')
        if selected_disease:
            remedies = get_remedies(selected_disease)
    return render_template('remedies.html', selected_disease=selected_disease, remedies=remedies)

if __name__ == '__main__':
    app.run(debug=True)
