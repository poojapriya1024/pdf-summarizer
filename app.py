from flask import Flask, render_template, request
import PyPDF2
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

app = Flask(__name__)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def summarize(text):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    tokens = [token.text for token in doc]
    punctuation_symbols = punctuation + '\\n'

    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation_symbols:
            word_frequencies[word.text] = word_frequencies.get(word.text, 0) + 1

    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] /= max_frequency

    sentence_tokens = [sentence for sentence in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word.text.lower()]

    select_length = int(len(sentence_tokens) * 0.5)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = " ".join(final_summary)  # Join directly into a final summary
    return summary

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
            summary = summarize(text)
        else:
            print("The PDF you have uploaded is empty")
            return render_template("index.html")
    return summary

if __name__ == '__main__':
    app.run(debug=1)