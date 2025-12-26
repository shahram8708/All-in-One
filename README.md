# All-in-One AI Web Platform

This project is a comprehensive Flask-based web application that bundles multiple AI-powered tools into a single platform. It integrates with Google Generative AI models to provide features such as chatting with an AI assistant, text-based querying, PDF summarization and interaction, code generation, math assistance, and YouTube video transcript summarization.

---

## Overview

The application runs a Flask server and serves dedicated web interfaces for each tool. All AI capabilities are powered using the Google Generative AI API, while additional utilities like PDF handling and YouTube transcript extraction enhance functionality.

The platform includes the following modules:

* **Code Generator** – AI-powered coding assistance and generation
* **BrieflyPDF** – Summarize uploaded PDF content
* **ChatMaven** – Interactive conversational chatbot
* **DoubtClear** – General question answering assistant
* **Math Assistant** – Solve mathematical queries
* **PDFVisionary** – Advanced PDF interaction and processing
* **QueryVista** – Text querying and processing
* **Video Summarizer** – Summarize YouTube video transcripts
* **VidSage** – Additional AI-powered video transcript interaction

Each tool has its own dedicated UI page.

---

## Features

* AI-powered conversational chat
* PDF upload, reading, and summarization
* AI-based PDF interaction utilities
* General knowledge and doubt-solving assistant
* Code generation tool
* Math problem solver
* Text query processing
* YouTube video transcript extraction and summarization
* Support for file uploads and downloads
* CORS enabled
* Clean and structured HTML interfaces

---

## Tech Stack

* **Backend:** Flask
* **AI Integration:** Google Generative AI (`google-generativeai`)
* **PDF Processing:** PyPDF2, markdown2, fpdf
* **YouTube Transcript:** youtube-transcript-api
* **HTTP / Utilities:** requests, base64, tempfile, logging
* **Frontend:** HTML, CSS, JavaScript
* **Deployment:** gunicorn support available

---

## Project Structure

```
All-in-One-main/
│
├── app.py                     # Core Flask backend and API integrations
├── requirements.txt           # Python dependencies
│
├── index.html                 # Landing UI
├── code.html                  # Code Generator UI
├── brieflypdf.html            # PDF summarizer UI
├── chatmaven.html             # Chat interface
├── doubtclear.html            # General query UI
├── math.html                  # Math assistant UI
├── pdfvisionary.html          # PDF processing UI
├── queryvista.html            # Text query UI
├── videosummarize.html        # Video summarizer UI
└── vidsage.html               # Video AI assistant UI
```

---

## Installation

1. Ensure Python is installed.
2. Extract the project folder.
3. Open a terminal inside the project directory.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

The application requires a valid Google Generative AI API key.

Set the environment variable before running the app:

**Linux / macOS**

```bash
export API_KEY="YOUR_API_KEY"
```

**Windows (PowerShell)**

```powershell
setx API_KEY "YOUR_API_KEY"
```

The application internally references:

```python
genai.configure(api_key=os.environ['API_KEY'])
```

Internet access is required for all AI and YouTube functionalities.

---

## Running the Application

Start the Flask server:

```bash
python app.py
```

The application runs in debug mode.
Open your browser and visit:

```
http://127.0.0.1:5000
```

From the home page, you can navigate to each tool's dedicated interface.

---

## Usage Summary

* Navigate to the desired tool from the landing page.
* Provide the required input (text, PDF file upload, or YouTube link depending on the feature).
* Submit the request.
* View AI-generated results in the same interface.
* Where applicable, PDF responses can be downloaded.

---

## Dependencies

Dependencies are listed in `requirements.txt`, including:

* Flask
* google-generativeai
* PyPDF2
* flask-cors
* youtube-transcript-api
* fpdf
* markdown / markdown2
* requests
* gunicorn

---

## Notes

* A valid Google Generative AI API key is required.
* The application depends on internet connectivity.
* PDF tools accept PDF files only.
* YouTube features rely on transcript availability.
* Some endpoints handle file uploads and generate downloadable responses.

---

## License

No license file is included in this project.
