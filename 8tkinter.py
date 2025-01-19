import os
import json
import spacy
import fitz
from tkinter import Tk, filedialog, Label, Button, Text, Scrollbar, END
from transformers import pipeline
from bs4 import BeautifulSoup

# Load SpaCy and Transformers models
nlp = spacy.load("en_core_web_sm")
llm = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Function to parse HTML files
def html(fp):
    with open(fp, 'r') as f:
        s = BeautifulSoup(f, 'html.parser')
    return s.get_text()

# Function to parse PDF files
def pdf(fp):
    d = fitz.open(fp)
    t = ""
    for p in range(d.page_count):
        j = d.load_page(p)
        t += j.get_text("text")
    return t

# Function to extract information using the LLM
def exll(k, l):
    r = llm(question=l, context=k)
    return r['answer']

# Function to extract specific fields from the text
def exin(t):
    tabinfo = [
        "Bid Number", "Title", "Due Date", "Bid Submission Type", 
        "Term of Bid", "Pre Bid Meeting", "Installation", "Bid Bond Requirement", 
        "Delivery Date", "Payment Terms", "Any Additional Documentation Required", 
        "MFG for Registration", "Contract or Cooperative to use", "Model_no", 
        "Part_no", "Product", "contact_info", "company_name", "Bid Summary", 
        "Product Specification"
    ]
    d = {}
    for h in tabinfo:
        q = f"What is the {h}?"
        a = exll(t, q)
        d[h] = a
    return d

# Function to generate JSON from the extracted data
def json_output(d):
    return json.dumps(d, indent=4)

# Function to process the uploaded document
def docs(fp, ft="html"):
    if ft == "html":
        t = html(fp)
    elif ft == "pdf":
        t = pdf(fp)
    else:
        raise ValueError("Unsupported file type")
    
    d = exin(t)
    j = json_output(d)
    out = "extract_data.json"
    with open(out, "w") as g:
        g.write(j)
    return j

# Function to handle file upload and processing
def upload(outp):
    file = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("HTML and PDF files", "*.html *.pdf"), ("All files", "*.*")]
    )
    if file:
        file_type = "pdf" if file.endswith(".pdf") else "html" if file.endswith(".html") else None
        if file_type is None:
            outp.insert(END, "Unsupported file type\n")
            return
        try:
            res = docs(file, ft=file_type)
            outp.insert(END, "File processing successful\n")
            outp.insert(END, f"Extracted Data:\n{res}\n")
        except Exception as e:
            outp.insert(END, f"Error processing file: {e}\n")
    else:
        outp.insert(END, "No file selected\n")

# Function to create the GUI
def gui():
    root = Tk()
    root.title("PDF/HTML Processor")
    root.geometry("800x600")
    
    Label(root, text="Select a PDF or HTML file to process:", font=("Helvetica", 14)).pack(pady=10)
    Button(root, text="Upload and Process File", command=lambda: upload(output_text), font=("Helvetica", 12)).pack(pady=5)
    
    output_frame = Scrollbar(root)
    output_frame.pack(side="right", fill="y")
    
    output_text = Text(root, wrap="word", yscrollcommand=output_frame.set, font=("Courier", 10), bg="#f5f5f5", relief="sunken", borderwidth=2)
    output_text.pack(expand=True, fill="both", padx=10, pady=10)
    
    output_frame.config(command=output_text.yview)
    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    gui()
