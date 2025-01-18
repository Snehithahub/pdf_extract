import os
import json
import re
from pypdf import PdfReader
from bs4 import BeautifulSoup
from transformers import pipeline
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Function to extract text from a PDF file
def ex_tx_pdf(pdf_pth):
    rd = PdfReader(pdf_pth)
    tp = len(rd.pages)
    print(f"Total number of pages: {tp}")
    
    etx = ""
    for pi in range(tp):
        pg = rd.pages[pi]
        etx += pg.extract_text()
    
    return etx

# Function to extract text from an HTML file
def ex_tx_html(html_pth):
    with open(html_pth, "r", encoding="utf-8") as fl:
        html_ct = fl.read()
    sp = BeautifulSoup(html_ct, "html.parser")
    return sp.get_text()

# Initialize NLP pipeline for Named Entity Recognition (NER)
nlp_ner = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", tokenizer="dbmdz/bert-large-cased-finetuned-conll03-english")

# Function to extract bid data using NLP
def ex_bd_dt(tx):
    # Run NER on the extracted text
    ner_results = nlp_ner(tx)
    
    # Fields mapping based on the expected output format
    bd_dt = {
        "Bid Number": None,
        "Title": None,
        "Due Date": None,
        "Bid Submission Type": None,
        "Term of Bid": None,
        "Pre Bid Meeting": None,
        "Installation": None,
        "Bid Bond Requirement": None,
        "Delivery Date": None,
        "Payment Terms": None,
        "Any Additional Documentation Required": None,
        "MFG for Registration": None,
        "Contract or Cooperative to use": None,
        "Model_no": None,
        "Part_no": None,
        "Product": None,
        "Contact Info": None,
        "Company Name": None,
        "Bid Summary": None,
        "Product Specification": None
    }
    
    # Map the NER results to the relevant fields
    for entity in ner_results:
        # Iterate through each entity and map it to the appropriate field
        if entity['word'].lower() == "bid" and bd_dt["Bid Number"] is None:
            bd_dt["Bid Number"] = entity['word']
        elif entity['entity'] == "ORG" and bd_dt["Company Name"] is None:
            bd_dt["Company Name"] = entity['word']
        elif entity['entity'] == "DATE" and bd_dt["Due Date"] is None:
            bd_dt["Due Date"] = entity['word']
        elif entity['entity'] == "MISC" and bd_dt["Bid Submission Type"] is None:
            bd_dt["Bid Submission Type"] = entity['word']
    
    return bd_dt

# Main function to process the file and output bid details in JSON format
def pr_doc(fp):
    # Check the file extension and extract text based on file type
    if fp.endswith(".pdf"):
        tx = ex_tx_pdf(fp)
    elif fp.endswith(".html"):
        tx = ex_tx_html(fp)
    else:
        raise ValueError("Unsupported file format. Only HTML and PDF files are supported.")
    
    # Extract structured bid details using NLP
    bd_dt = ex_bd_dt(tx)

    # Convert the bid details to JSON format for easy use
    return json.dumps(bd_dt, indent=4)

# Example of how to use the functions
if __name__ == "__main__":
    fp = r'C:\Users\Chandra\Downloads\2025 assignment-20241122T122913Z-001\Campus hiring-2024-2025 assignment\Bid1\Addendum 1 RFP JA-207652 Student and Staff Computing Devices.pdf'
    
    try:
        # Process the document and retrieve the structured bid details
        str_dt = pr_doc(fp)
        
        # Print the bid details in JSON format
        print(str_dt)
        
        # Optionally save the structured bid data to a JSON file
        with open("str_bd_info.json", "w") as js_fl:
            js_fl.write(str_dt)
    
    except Exception as err:
        print(f"An error occurred: {err}")
