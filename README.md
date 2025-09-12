# Document Q&A AI Agent

This project implements a Document Q&A AI Agent that can ingest multiple PDF documents, extract their content, and answer user queries based on the documents. It also includes a feature to search for papers on Arxiv.

## Features

- **PDF Document Ingestion**: Handles multiple PDF documents, extracting text and structure.
- **NLP-Powered Q&A**: Allows users to ask questions about the ingested documents.
- **Summarization**: Can summarize key insights from the documents.
- **Specific Information Extraction**: Can extract specific results like evaluation metrics.
- **Arxiv Integration**: Can search for papers on Arxiv using a user's description.

## Setup Instructions

Prerequisites:
- Python 3.10+
- Git

1) Create and activate a virtual environment
- PowerShell (Windows):
    ```powershell
    py -3.10 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```
    If activation is blocked, temporarily allow scripts:
    ```powershell
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\.venv\Scripts\Activate.ps1
    ```
- macOS/Linux:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2) Install dependencies
```bash
pip install -r requirements.txt
```

3) Optional: Hugging Face token (only if using remote endpoints)
- By default, the app uses a local Transformers model (`google/flan-t5-base`) and will download weights on first run.
- If you prefer using Hugging Face Inference Endpoints, create a `.env` file with:
    ```
    HUGGINGFACEHUB_API_TOKEN=your_hugging_face_api_token
    ```

4) Add your documents
Place PDFs into the `documents/` folder (a sample file may already be included).

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
