import streamlit as st
import fitz 
import docx
import tempfile
from io import BytesIO

def extract_text_from_pdf(file):
    pdf_text = ""
    if file is not None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = f"{temp_dir}/uploaded_file.pdf"

            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(file.read())

            with fitz.open(temp_file_path) as pdf_document:
                for page_number in range(len(pdf_document)):
                    page = pdf_document[page_number]
                    pdf_text += page.get_text()

    return pdf_text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

def extract_text_from_txt(file):
    return file.read().decode("utf-8")

st.title("Document Reader")

st.write("Upload a document (PDF, DOCX, or TXT) to read its text content.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == "pdf":
        text = extract_text_from_pdf(uploaded_file)
    elif file_type == "docx":
        text = extract_text_from_docx(uploaded_file)
    elif file_type == "txt":
        text = extract_text_from_txt(uploaded_file)
    else:
        text = "Unsupported file type"

    st.header("Extracted Text:")
    st.text_area("Text from the document:", text, height=500)
