from flask import Flask, request, render_template, send_file
from PyPDF2 import PdfReader, PdfWriter

import os, io, secrets
from werkzeug.exceptions import RequestEntityTooLarge


app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"))

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")
@app.errorhandler(RequestEntityTooLarge)
def largefile(e):
    return "too large file,pls upload lower than 40mb",413  
def encryptpdf(filestream,password):
        pdf_reader=PdfReader(filestream)
        pdf_writer=PdfWriter()
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        pdf_writer.encrypt(password)

        output_stream=io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        return output_stream
@app.route('/upload',methods=['POST'])
def upload():
    file=request.files.get("file")
    password=request.form.get("password")

    if not file or not password:
        return "FILE AND PASSWORD MUST BE UPLOADED"
    output_stream=encryptpdf(file.stream,password)
    return send_file(output_stream,as_attachment=True,download_name=secrets.token_hex(4)+".pdf"
                         ,mimetype="application/pdf")
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
