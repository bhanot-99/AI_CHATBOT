from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def process_pdf(file):
    from PyPDF2 import PdfReader
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return process_text(text)