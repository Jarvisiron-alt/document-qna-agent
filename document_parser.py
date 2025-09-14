import os
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a single PDF file.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def process_documents(directory):
    """
    Processes all PDF documents in a given directory.
    Extracts text and splits it into manageable chunks.
    """
    processed_docs = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)

    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            print(f"Processing {filename}...")
            
            raw_text = extract_text_from_pdf(pdf_path)
            
            if raw_text:
                chunks = text_splitter.split_text(raw_text)
                
                for i, chunk in enumerate(chunks):
                    processed_docs.append({
                        "source": filename,
                        "content": chunk,
                        "chunk_id": i
                    })
    return processed_docs
