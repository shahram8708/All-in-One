import os
from flask import Flask, render_template, request, jsonify, send_file
import google.generativeai as genai
import markdown
import PyPDF2
from flask_cors import CORS
import base64
import logging
import tempfile
import time
from youtube_transcript_api import YouTubeTranscriptApi
from fpdf import FPDF
import markdown2
import io
import requests
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)
CORS(app)
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
genai.configure(api_key=os.environ['API_KEY'])
API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyBc9a2I57vkHjVYhJ42QkzMxZvwq0BY44k"
API_KEY = "AIzaSyBPgXeivnFmtX6-PSu3XudU0-EraotrYf4"
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/code', methods=['GET', 'POST'])
def code():
    return render_template('code.html')

@app.route('/brieflypdf', methods=['GET', 'POST'])
def brieflypdf():
    return render_template('brieflypdf.html')

@app.route('/chatmaven', methods=['GET', 'POST'])
def chatmaven():
    return render_template('chatmaven.html')

@app.route('/doubtclear', methods=['GET', 'POST'])
def doubtclear():
    return render_template('doubtclear.html')

@app.route('/math', methods=['GET', 'POST'])
def math():
    return render_template('math.html')

@app.route('/pdfvisionary', methods=['GET', 'POST'])
def pdfvisionary():
    return render_template('pdfvisionary.html')

@app.route('/queryvista', methods=['GET', 'POST'])
def queryvista():
    return render_template('queryvista.html')

@app.route('/videosummarize', methods=['GET', 'POST'])
def videosummarize():
    return render_template('videosummarize.html')

@app.route('/vidsage', methods=['GET', 'POST'])
def vidsage():
    return render_template('vidsage.html')

@app.route('/chat', methods=['POST'])
def chat_response():
    user_input = request.form['user_input']
    if user_input.lower() != 'exit':
        response = chat.send_message(user_input)
        bot_response = response.text 
        bot_response_html = markdown.markdown(bot_response)
    else:
        bot_response_html = markdown.markdown("Chat ended. Please refresh the page to start a new chat.")
    
    return jsonify(user_input=user_input, bot_response=bot_response_html)

@app.route('/pdfprocess', methods=['POST'])
def pdfprocess():
    try:
        uploaded_files = request.files.getlist("images")
        prompt = request.form.get("prompt")

        images = []
        for file in uploaded_files:
            image_data = {
                'mime_type': file.content_type,
                'data': file.read()
            }
            images.append(image_data)

        response = genai.GenerativeModel('gemini-1.5-flash').generate_content([prompt] + images)
        markdown_text = response.text

        html_text = markdown.markdown(markdown_text)

        return jsonify({"html": html_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_pdf(file_stream):
    reader = PyPDF2.PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

@app.route('/fullresponse')
def fullresponse():
    return render_template('fullresponse.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files or 'prompt' not in request.form:
        return jsonify({'error': 'No files or prompt provided'}), 400

    files = request.files.getlist('files[]')
    prompt = request.form['prompt']
    pdf_texts = []

    for file in files:
        if file and allowed_file(file.filename):
            file_stream = io.BytesIO(file.read())
            pdf_texts.append(extract_text_from_pdf(file_stream))

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([prompt] + pdf_texts)
    
    response_text = response.text

    return jsonify({'response': response_text})

@app.route('/generate_content', methods=['POST'])
def generate_content():
    try:
        payload = request.json
        logging.debug("Request payload: %s", payload)

        if 'contents' not in payload or not payload['contents']:
            return jsonify({'error': 'Invalid request payload.'}), 400

        image_base64 = payload['contents'][0]['parts'][1]['inlineData']['data']
        image_data = base64.b64decode(image_base64)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()
        logging.debug("Response JSON: %s", response_json)

        generated_content = response_json.get('candidates')[0]['content']['parts'][0]['text']

        if generated_content:
            html_content = markdown.markdown(generated_content)
            return jsonify({'generated_content': html_content})
        else:
            return jsonify({'error': 'Failed to generate content.'}), 500

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        return jsonify({'error': 'Internal Server Error.'}), 500

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, POST'
    return response

@app.route('/queryprocess', methods=['POST'])
def queryprocess():
    try:
        uploaded_files = request.files.getlist("images")
        prompt = request.form.get("prompt")

        images = []
        for file in uploaded_files:
            image_data = {
                'mime_type': file.content_type,
                'data': file.read()
            }
            images.append(image_data)

        response = genai.GenerativeModel('gemini-1.5-flash').generate_content([prompt] + images)
        markdown_text = response.text

        html_text = markdown.markdown(markdown_text)

        return jsonify({"html": html_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    video_id = data['videoId']
    prompt_text = data['promptText']
    try:
        transcript = get_transcript(video_id)
        gemini_response = generate_story(prompt_text + transcript)
        logging.debug(f"API response: {gemini_response}")
        if gemini_response and 'candidates' in gemini_response:
            story_content = extract_story_content(gemini_response)
            if story_content:
                markdown_content = markdown2.markdown(story_content)
                return jsonify({'summary': markdown_content})
        return jsonify({'error': 'Failed to generate story content. Please try again.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = ' '.join([t['text'] for t in transcript])
        return text.strip()
    except Exception as e:
        raise Exception('Failed to fetch transcript: ' + str(e))

def generate_story(prompt):
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(API_ENDPOINT, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def extract_story_content(response):
    candidates = response['candidates']
    if candidates:
        content = candidates[0]['content']
        if content:
            parts = content['parts']
            if parts:
                return parts[0].get('text', '')
    return None

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    data = request.json
    text = data['text']
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        filename = tmpfile.name
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)
        pdf.output(filename)

    response = send_file(filename, as_attachment=True, download_name="transcript.pdf")
    
    try:
        time.sleep(1)
        os.remove(filename)
    except Exception as e:
        print(f"Error deleting the file: {e}")
    
    return response

@app.route('/vidupload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = os.path.join('uploads', file.filename)
    file.save(filename)

    try:
        file_data, video_file = upload_and_process_video(filename)
        custom_input = request.form.get('customInput', '')
        response = generate_content(file_data, custom_input)
        delete_file(file_data)

        markdown_content = response.text
        html_content = markdown.markdown(markdown_content)
        
        return jsonify({'summary': html_content})
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'error': 'Failed to generate response. Please try again.'}), 500

def upload_and_process_video(video_file_name):
    print(f"Uploading file...")
    video_file = genai.upload_file(path=video_file_name)
    print(f"Completed upload: {video_file.uri}")

    while video_file.state.name == "PROCESSING":
        print('.', end='', flush=True)
        time.sleep(10) 
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError(f"File processing failed: {video_file.state.name}")

    file = genai.get_file(name=video_file.name)
    print(f"Retrieved file '{file.display_name}' as: {video_file.uri}")

    return file, video_file

def generate_content(file, prompt):
    print("Making LLM inference request...")
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    response = model.generate_content([file, prompt], request_options={"timeout": 600})
    print(response.text)
    return response

def delete_file(file):
    print(f'Deleting file {file.uri}')
    genai.delete_file(file.name)
    print(f'Deleted file {file.uri}')

@app.route('/generatecontent', methods=['POST'])
def generatecontent():
    try:
        payload = request.json
        logging.debug("Request payload: %s", payload)

        if 'contents' not in payload or not payload['contents']:
            return jsonify({'error': 'Invalid request payload.'}), 400

        image_base64 = payload['contents'][0]['parts'][1]['inlineData']['data']
        image_data = base64.b64decode(image_base64)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()
        logging.debug("Response JSON: %s", response_json)

        generated_content = response_json.get('candidates')[0]['content']['parts'][0]['text']

        cleaned_content = generated_content.replace('*', '')

        if cleaned_content:
            return jsonify({'generated_content': cleaned_content})
        else:
            return jsonify({'error': 'Failed to generate content.'}), 500

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        return jsonify({'error': 'Internal Server Error.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
