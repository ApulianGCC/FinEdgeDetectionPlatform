from flask import Flask, flash, request, redirect, url_for, render_template
import eval
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/input/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def main():
    return render_template("index.html", title="Test Falsk")

@app.route("/output", methods=['GET', 'POST'])
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
            print('ciao')
            filename = secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER'] + filename)
            #return redirect(url_for('download_file', name=filename))
    return render_template("index.html", title="Test Falsk")

if __name__ == "__main__":
    app.run(debug=True, port=5000)