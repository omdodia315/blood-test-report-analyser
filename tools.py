import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

def read_data_tool(path='data/sample.pdf'):
    """Reads data from a PDF file and returns text"""
    try:
        loader = PyPDFLoader(path)
        docs = loader.load()
        content = "\n".join([doc.page_content for doc in docs])
        return content.strip() if content else "Empty PDF"
    except Exception as e:
        return f"Failed to load PDF: {str(e)}"
