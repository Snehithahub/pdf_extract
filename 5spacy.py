import os
import json
import re
import spacy
from pypdf import PdfReader
from bs4 import BeautifulSoup

nlp = spacy.load("en_core_web_sm")

def ex_tx_pdf(pth):
    rd = PdfReader(pth)
    tp = len(rd.pages)
    etx = ""
    for pi in range(tp):
        pg = rd.pages[pi]
        etx += pg.extract_text()
    return etx

def ex_tx_html(pth):
    with open(pth, "r", encoding="utf-8") as fl:
        ct = fl.read()
    sp = BeautifulSoup(ct, "html.parser")
    return sp.get_text()

def cl_tx(tx):
    doc = nlp(tx)
    ct = ' '.join([t.text for t in doc if t.is_alpha or t.is_digit])
    return ct

def ex_bd_dt(tx):
    pt = {
        "Bid Number": r"Bid Number[:\s]*([A-Za-z0-9\-]+)",
        "Title": r"Title[:\s]*([A-Za-z0-9\s\-,]+)",
        "Due Date": r"Due Date[:\s]*([\d/]+)",
        "Bid Submission Type": r"Bid Submission Type[:\s]*([A-Za-z\s]+)",
        "Term of Bid": r"Term of Bid[:\s]*([A-Za-z0-9\s]+)",
        "Pre Bid Meeting": r"Pre Bid Meeting[:\s]*([A-Za-z\s]+)",
        "Installation": r"Installation[:\s]*([A-Za-z\s]+)",
        "Bid Bond Requirement": r"Bid Bond Requirement[:\s]*([A-Za-z\s]+)",
        "Delivery Date": r"Delivery Date[:\s]*([\d/]+)",
        "Payment Terms": r"Payment Terms[:\s]*([A-Za-z0-9\s]+)",
        "Any Additional Documentation Required": r"Any Additional Documentation Required[:\s]*([A-Za-z\s]+)",
        "MFG for Registration": r"MFG for Registration[:\s]*([A-Za-z0-9\s]+)",
        "Contract or Cooperative to use": r"Contract or Cooperative to use[:\s]*([A-Za-z0-9\s]+)",
        "Model_no": r"Model No[:\s]*([A-Za-z0-9\-]+)",
        "Part_no": r"Part No[:\s]*([A-Za-z0-9\-]+)",
        "Product": r"Product[:\s]*([A-Za-z0-9\s\-]+)",
        "Contact Info": r"Contact Info[:\s]*([A-Za-z0-9\s\-\+]+)",
        "Company Name": r"Company Name[:\s]*([A-Za-z0-9\s]+)",
        "Bid Summary": r"Bid Summary[:\s]*([A-Za-z0-9\s\-,]+)",
        "Product Specification": r"Product Specification[:\s]*([A-Za-z0-9\s\-,]+)"
    }

    bd_dt = {}
    for fd, pt in pt.items():
        mt = re.search(pt, tx, re.IGNORECASE)
        if mt:
            bd_dt[fd] = mt.group(1).strip()
        else:
            bd_dt[fd] = "Not Available"
    
    return bd_dt

def pr_doc(fp):
    if fp.endswith(".pdf"):
        tx = ex_tx_pdf(fp)
    elif fp.endswith(".html"):
        tx = ex_tx_html(fp)
    else:
        raise ValueError("Unsupported file format. Only HTML and PDF files are supported.")
    
    ct = cl_tx(tx)
    bd_dt = ex_bd_dt(ct)
    return json.dumps(bd_dt, indent=4)

if __name__ == "__main__":
    fp = r'C:\Users\Chandra\Downloads\2025 assignment-20241122T122913Z-001\Campus hiring-2024-2025 assignment\Bid1\Addendum 1 RFP JA-207652 Student and Staff Computing Devices.pdf'

    try:
        str_dt = pr_doc(fp)
        print(str_dt)
        with open("str_bd_info.json", "w") as js_fl:
            js_fl.write(str_dt)

    except Exception as err:
        print(f"An error occurred: {err}")
