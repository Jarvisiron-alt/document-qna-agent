import os
from document_parser import process_documents
from qa_interface import QASystem
from arxiv_client import ArxivClient
from dotenv import load_dotenv

def main():
    
    load_dotenv()
    api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not api_key:
        print("Error: HUGGINGFACEHUB_API_TOKEN environment variable not set.")
        print("Please set it to your Hugging Face API token.")
        return


    doc_directory = "documents"
    if not os.path.exists(doc_directory):
        os.makedirs(doc_directory)
        print(f"Created directory: {doc_directory}")
        print("Please add your PDF documents to this directory.")
        return

    
    print("Starting document ingestion...")
    processed_docs = process_documents(doc_directory)
    if not processed_docs:
        print("No documents processed. Exiting.")
        return
    print(f"Successfully processed {len(processed_docs)} documents.")

    qa_system = QASystem(processed_docs, api_key)
    arxiv_client = ArxivClient()

    print("\nDocument Q&A AI Agent")
    print("Ask questions about the documents or use 'arxiv:' to search for a paper.")
    print("Type 'exit' to quit.")

    while True:
        query = input("\nEnter your query: ")

        if query.lower() == 'exit':
            break

        if query.lower().startswith('arxiv:'):
            search_query = query[len('arxiv:'):].strip()
            print(f"Searching Arxiv for: '{search_query}'")
            papers = arxiv_client.search_papers(search_query)
            if papers:
                for i, paper in enumerate(papers):
                    print(f"\n{i+1}. Title: {paper['title']}")
                    print(f"   Authors: {', '.join(paper['authors'])}")
                    print(f"   Published: {paper['published']}")
                    print(f"   Summary: {paper['summary']}")
            else:
                print("Could not find any papers matching your description.")
        else:
            response = qa_system.ask_question(query)
            print(f"\nAnswer: {response}")

if __name__ == "__main__":
    main()
