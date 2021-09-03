from flask import Flask,session, flash, request, redirect, url_for, render_template, send_from_directory
from flask_dropzone import Dropzone
import eval
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'input/'
OUTPUT_FOLDER = 'output/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = os.urandom(16)
dropzone = Dropzone(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*, .jpg, .jpeg'
app.config['DROPZONE_MAX_FILE_SIZE'] = 16 * 1024 * 1024
app.config['DROPZONE_MAX_FILES'] = 1
app.config[ 'DROPZONE_DEFAULT_MESSAGE'] = 'Drag & Drop your file here' \
                                          '<br>or<br>' \
                                          '<button type="button">Click to Upload</button>'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def main():
    session.pop('file_name', None)
    return render_template("index.html", title="Test Falsk")
    return render_template("index.html", title="Fin Edge Detection")

@app.route("/info")
def info():
    return render_template("info.html", title="Fin Edge Detection")


@app.route('/uploads', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'] + filename))
            session['file_name'] = filename
    return 'uploaded'


@app.route('/get_outline')
def get_outline():
    file_name = session.get('file_name')
    if file_name is not None:
        eval.run(file_name)
        return render_template("result.html", title="result", filename=file_name)
    else:
        flash('devi caricare una foto trmn')

    return redirect(request.url)

'''
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
'''


@app.route('/input/<filename>')
def send_image_input(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route('/output/<filename>')
def send_image_output(filename):
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename.replace('jpg', 'png'))


if __name__ == "__main__":
    eval.load_model()
    app.run(debug=True, port=5000)
