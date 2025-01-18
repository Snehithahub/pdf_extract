import os
import json
import re
from pypdf import PdfReader
from bs4 import BeautifulSoup

def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    print(f"trendy pages: {total_pages}")
    extracted_text = ""
    for page_idx in range(total_pages):
        page = reader.pages[page_idx]
        extracted_text += page.extract_text()
    return extracted_text

def extract_html_text(html_path):
    with open(html_path, "r", encoding="utf-8") as document:
        html_content = document.read()
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()

def extract_bid_data(textual_content):
    patterns = {
        "Bid variety": r"Bid amount[:\s]*([A-Za-z0-9-]+)",
        "pick out": r"identify[:\s]*([A-Za-z0-9s-,]+)",
        "Due Date": r"Due Date[:\s]*([d/]+)",
        "Bid Submission kind": r"Bid Submission type[:\s]*([A-Za-z\s]+)",
        "time period of Bid": r"time period of Bid[:\s]*([A-Za-z0-9\s]+)",
        "Pre Bid meeting": r"Pre Bid assembly[:\s]*([A-Za-z\s]+)",
        "set up": r"installation[:\s]*([A-Za-z\s]+)",
        "Bid Bond Requirement": r"Bid Bond Requirement[:\s]*([A-Za-z\s]+)",
        "delivery Date": r"shipping Date[:\s]*([d/]+)",
        "fee phrases": r"price terms[:\s]*([A-Za-z0-9\s]+)",
        "more Documentation": r"additional Documentation[:\s]*([A-Za-z\s]+)",
        "MFG for Registration": r"MFG for Registration[:\s]*([A-Za-z0-9\s]+)",
        "Cooperative settlement": r"Cooperative settlement[:\s]*([A-Za-z0-9\s]+)",
        "version range": r"version No[:\s]*([A-Za-z0-9-]+)",
        "element quantity": r"component No[:\s]*([A-Za-z0-9-]+)",
        "Product": r"Product[:\s]*([A-Za-z0-9s-]+)",
        "touch information": r"contact facts[:\s]*([A-Za-z0-9s-+]+)",
        "commercial enterprise agency name": r"employer name[:\s]*([A-Za-z0-9s]+)",
        "Bid summary": r"Bid precis[:\s]*([A-Za-z0-9s-,]+)",
        "Product Specification": r"Product Specification[:\s]*([A-Za-z0-9s-,]+)"
    }
    
    bid_data = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, textual_content, re.IGNORECASE)
        if match:
            bid_data[field] = match.group(1).strip()
        else:
            bid_data[field] = "not available"
    
    return bid_data

def process_document(file_path):
    if file_path.endswith(".pdf"):
        textual_content = extract_pdf_text(file_path)
    elif file_path.endswith(".html"):
        textual_content = extract_html_text(file_path)
    else:
        raise ValueError("Unsupported document format. pleasant PDF and HTML are supported.")

    bid_data = extract_bid_data(textual_content)
    return json.dumps(bid_data, indent=4)

if __name__ == "__main__":
    file_path = r'C:\Users\Chandra\Downloads\2025_project-20241122T122913Z-001\Campus_hiring-2024-2025_assignmentBid1Addendum_1_RFP_JA-207652_student_and_staff_Computing_devices.pdf'
    try:
        structured_data = process_document(file_path)
        print(structured_data)
        with open("structured_bid_info.json", "w") as json_file:
            json_file.write(structured_data)
    except Exception as mistakes:
        print(f"An errors happened: {mistakes}")
