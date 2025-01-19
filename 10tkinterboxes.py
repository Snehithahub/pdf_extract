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
    
    return j

# Function to handle file upload and processing
def process_file(input_file, output_location):
    if not os.path.exists(input_file):
        return f"Input file '{input_file}' does not exist."

    file_type = "pdf" if input_file.endswith(".pdf") else "html" if input_file.endswith(".html") else None
    if file_type is None:
        return "Unsupported file type. Only .html and .pdf are supported."

    try:
        res = docs(input_file, ft=file_type)
        json_filename = os.path.join(output_location, f"{os.path.basename(input_file)}.json")

        # Save the data to the specified location
        with open(json_filename, "w") as g:
            g.write(res)

        return f"File processing successful. Data saved in: {json_filename}\nExtracted Data:\n{res}"
    except Exception as e:
        return f"Error processing file: {e}"

# Function to create the GUI
def gui():
    root = Tk()
    root.title("PDF/HTML Processor")
    root.geometry("800x600")
    
    # Instructions Label
    Label(root, text="Enter the location of the PDF/HTML file:", font=("Helvetica", 14)).pack(pady=10)
    
    # Input Textbox for file location
    input_text = Text(root, height=2, font=("Courier", 10), bg="#f5f5f5", relief="sunken", borderwidth=2)
    input_text.pack(fill="x", padx=10, pady=10)
    
    # Label for output location
    Label(root, text="Enter the directory to save the output JSON file:", font=("Helvetica", 14)).pack(pady=10)
    
    # Input Textbox for output location
    output_text = Text(root, height=2, font=("Courier", 10), bg="#f5f5f5", relief="sunken", borderwidth=2)
    output_text.pack(fill="x", padx=10, pady=10)
    
    # Output Textbox for displaying results
    result_text = Text(root, wrap="word", font=("Courier", 10), bg="#f5f5f5", relief="sunken", borderwidth=2)
    result_text.pack(expand=True, fill="both", padx=10, pady=10)

    def on_process_button_click():
        input_file = input_text.get("1.0", "end-1c").strip()
        output_location = output_text.get("1.0", "end-1c").strip()
        
        if not input_file or not output_location:
            result_text.insert(END, "Please provide both input file path and output directory.\n")
            return

        result = process_file(input_file, output_location)
        result_text.insert(END, result + "\n\n")

    # Process Button
    Button(root, text="Process File", command=on_process_button_click, font=("Helvetica", 12)).pack(pady=5)

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    gui()
