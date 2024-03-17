from flask import Flask, render_template, request
import PyPDF2
app = Flask(__name__)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    print(text)
    return text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    text = ""
    if request.method == "POST":
        pdf_path = request.form.get("pdf-path")
        print(pdf_path)
        if pdf_path:
            text = extract_text_from_pdf(pdf_path)
        else:
            print("The PDF you have uploaded is empty")
    return text

if __name__ == '__main__':
    app.run(debug=1)