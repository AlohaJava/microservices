from flask import Flask,send_file
from docxtpl import DocxTemplate
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/get-file', methods=['POST'])
def send_filer():
    doc = DocxTemplate("1.docx")
    context = request.form
    doc.render(context)
    return send_file(doc)
    


if __name__ == '__main__':
    app.run(host='0.0.0.0')
