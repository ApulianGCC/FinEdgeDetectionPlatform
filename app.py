from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
import eval
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'input/'
OUTPUT_FOLDER = 'output/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def main():
    return render_template("index.html", title="Fin Edge Detection")

@app.route("/info")
def info():
    return render_template("info.html", title="Fin Edge Detection")

@app.route("/upload", methods=['GET', 'POST'])
def output():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER'] + filename)
            eval.run()
    return render_template("output.html", title="Test Falsk", filename=filename)

@app.route('/input/<filename>')
def send_image_input(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route('/output/<filename>')
def send_image_output(filename):
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename.replace('jpg','png'))

if __name__ == "__main__":
    eval.load_model()
    app.run(debug=True, port=5000)