!pip install spacy
!pip install pdf2image
!pip install PyMuPDF
!pip install beautifulsoup4
!pip install transformers
!pip install pytesseract
!pip install lxml
!pip install pdfminer.six
!pip install huggingface_hub

!python -m spacy download en_core_web_sm

import spacy
import fitz
from bs4 import BeautifulSoup
import json
from transformers import pipeline

nlp = spacy.load("en_core_web_sm")
llm = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

def p_html(fp):
    with open(fp, 'r') as f:
        s = BeautifulSoup(f, 'html.parser')
    return s.get_text()

def p_pdf(fp):
    d = fitz.open(fp)
    t = ""
    for p in range(d.page_count):
        pg = d.load_page(p)
        t += pg.get_text("text")
    return t

def e_llm(t, q):
    r = llm(question=q, context=t)
    return r['answer']

def e_info(t):
    flds = [
        "Bid Number", "Title", "Due Date", "Bid Submission Type", 
        "Term of Bid", "Pre Bid Meeting", "Installation", "Bid Bond Requirement", 
        "Delivery Date", "Payment Terms", "Any Additional Documentation Required", 
        "MFG for Registration", "Contract or Cooperative to use", "Model_no", 
        "Part_no", "Product", "contact_info", "company_name", "Bid Summary", 
        "Product Specification"
    ]
    
    d = {}
    for f in flds:
        q = f"What is the {f}?"
        a = e_llm(t, q)
        d[f] = a
    
    return d

def g_json(d):
    return json.dumps(d, indent=4)

def p_doc(fp, ft="html"):
    if ft == "html":
        t = p_html(fp)
    elif ft == "pdf":
        t = p_pdf(fp)
    else:
        raise ValueError("Unsupported file type")
    
    d = e_info(t)
    j = g_json(d)
    
    with open("extracted_data.json", "w") as f:
        f.write(j)

    return "Extraction Complete! JSON file created: extracted_data.json"

pdf_fp = "/content/Addendum 2 RFP JA-207652 Student and Staff Computing Devices.pdf"
print(p_doc(pdf_fp, ft="pdf"))
