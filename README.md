
PDF/HTML Processor
This is a Python application that processes PDF or HTML files, extracts specific information, and saves the data in JSON format. The application uses natural language processing models (SpaCy and Hugging Face Transformers) to extract the required information.

Features
Supports both PDF and HTML files.
Extracts predefined fields of information using a question-answering model.
Saves the extracted data as a JSON file in the specified directory.
Includes a graphical user interface (GUI) for ease of use.
Prerequisites
Make sure you have Python 3.7 or higher installed.

Installation
Clone or download this repository to your local machine:


git clone https://github.com/your-repository/pdf-html-processor.git
cd pdf-html-processor
Create and activate a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install the required dependencies:

bash
Copy
Edit
pip install spacy
pip install PyMuPDF
pip install beautifulsoup4
pip install transformers
pip install Tkinter
Download the SpaCy model:
python -m spacy download en_core_web_sm
How to Run
Open a terminal or command prompt.
Run the Python script to launch the GUI:

python app.py
In the GUI:

Enter the path to the PDF or HTML file you want to process.
Enter the directory where you want the JSON output to be saved.
Click the "Process File" button.
Once the process is complete, the output will be displayed in the GUI and saved as a JSON file in the specified directory.

Notes
Ensure the PDF or HTML file is readable and accessible before running the script.
The program is designed to handle structured data but may have limitations with poorly formatted files.
Troubleshooting
Error: Model not found. Ensure you have downloaded the SpaCy model using the command:

python -m spacy download en_core_web_sm
Error: Unsupported file type. Make sure the file is either a .pdf or .html file.
