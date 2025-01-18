import os
import json
import re
from pypdf import PdfReader
from bs4 import BeautifulSoup

# Function to extract text from a PDF file
def ex_tx_pdf(pdf_pth):
    # Create a PDF reader object
    rd = PdfReader(pdf_pth)
    
    # Get the total number of pages in the PDF
    tp = len(rd.pages)
    print(f"Total number of pages: {tp}")
    
    # Extract text from each page of the PDF
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

# Function to parse bid information from the extracted text
def ex_bd_dt(tx):
    # Define regular expressions to capture each relevant field
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

# Main function to process the file and output bid details in JSON format
def pr_doc(fp):
    # Check the file extension and extract text based on file type
    if fp.endswith(".pdf"):
        tx = ex_tx_pdf(fp)
    elif fp.endswith(".html"):
        tx = ex_tx_html(fp)
    else:
        raise ValueError("Unsupported file format. Only HTML and PDF files are supported.")

    # Extract structured bid details from the text
    bd_dt = ex_bd_dt(tx)

    # Convert the bid details to JSON format for easy use
    return json.dumps(bd_dt, indent=4)

# Example of how to use the functions
if __name__ == "__main__":
    # Specify the file path (can be a PDF or HTML file)
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
