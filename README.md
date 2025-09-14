# Document Q&A — Ask Your PDFs Questions

This app lets you drop in one or more PDF files and ask natural-language questions about them. It reads your documents, builds a quick index, and answers based only on what’s inside. It can also search arXiv when you ask it to.

## What it can do
- Read multiple PDFs and extract their text
- Answer questions grounded in your documents
- Summarize sections or entire papers
- Pull out metrics like accuracy or F1 if they’re in the text
- Search arXiv when you prefix your query with `arxiv:`

## Quick start (Windows / PowerShell)
Prereqs: Python 3.10+, Git (recommended)

1) Create and activate a virtual environment
```powershell
cd "c:\Users\YASHU\VS project\document-qna-agent"
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
```
If activation is blocked, temporarily allow scripts in this session:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies
```powershell
pip install -r requirements.txt
```

3) Add your PDFs
Put your files in the `documents` folder. A sample PDF may already be there.

4) Run the app
```powershell
python app.py
```
On the first run, the local language model (`google/flan-t5-base`) will download automatically. That might take a minute.

## How to ask questions
Type questions right into the prompt, for example:
- "What problem does this paper address?"
- "Summarize the methodology in 3 bullets."
- "What accuracy and F1-score are reported?"
- "arxiv: retrieval-augmented generation evaluation"

To exit, type `exit`.

## Optional: Hugging Face token (remote endpoints)
By default, everything runs locally using Transformers. If you want to try a Hugging Face Inference Endpoint instead, create a `.env` file and add your token:
```
HUGGINGFACEHUB_API_TOKEN=your_hugging_face_api_token
```

You can also switch the local model by setting an environment variable before launching:
```powershell
$env:LOCAL_T2T_MODEL = "google/flan-t5-small"  
python app.py
```

## Troubleshooting
- "Activation of venv is blocked": run the `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` command above and try again.
- "pip not recognized": ensure Python is on PATH; try `py -3.10 -m pip install -r requirements.txt`.
- First answer is slow: model weights and embeddings are being prepared; subsequent runs are faster.
- Running out of memory: try a lighter model, e.g., set `LOCAL_T2T_MODEL` to `google/flan-t5-small`.

## Project layout
- `app.py` — CLI entry point; loads docs and runs the Q&A loop
- `document_parser.py` — parses PDFs and chunks text for retrieval
- `qa_interface.py` — embeddings, vector store, and the local LLM pipeline
- `arxiv_client.py` — simple arXiv search helper (use with `arxiv:` queries)
- `requirements.txt` — Python package list
- `documents/` — put your PDFs here

## Usage

Run the main application:
```bash
python app.py
```

The application will first process the documents in the `documents` directory. Once that's done, you can start asking questions.

**Example Queries:**

-   "What is the conclusion of Paper X?"
-   "Summarize the methodology of Paper C."
-   "What are the accuracy and F1-score reported in Paper D?"
-   "arxiv: search for papers on large language models"

To exit the application, type `exit`.

## Code Structure

-   `app.py`: The main entry point of the application.
-   `document_parser.py`: Handles PDF parsing and text extraction.
-   `qa_interface.py`: Implements the Q&A system using LangChain and a vector store.
-   `arxiv_client.py`: Contains the logic for interacting with the Arxiv API.
-   `requirements.txt`: Lists the Python dependencies for the project.
-   `documents/`: Directory where you should place your PDF files.
