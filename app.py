from flask import Flask, session, flash, request, redirect, url_for, render_template, send_from_directory
from flask_dropzone import Dropzone
import eval
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'input/'
OUTPUT_FOLDER = 'output/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")
app = Flask(__name__, static_url_path="/static", static_folder=static_file_dir)
app.secret_key = os.urandom(16)
dropzone = Dropzone(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*, .jpg, .jpeg'
app.config['DROPZONE_MAX_FILE_SIZE'] = 16 * 1024 * 1024
app.config['DROPZONE_MAX_FILES'] = 1
app.config['DROPZONE_DEFAULT_MESSAGE'] = '<div class="dz-content">' \
                                         '<img class="dz-message-icon" src = "/static/res/dz-upload-icon.png" />' \
                                         '<p class="dz-message">Drag & Drop your file here' \
                                         '<br>or<br></p>' \
                                         '<a class= "dz-link">Click to Upload</a>' \
                                         '</div>'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def main():
    session.pop('file_name', None)
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


@app.route('/deletefile', methods=['POST'])
def delete_file():
    filename = session.pop('file_name', None)
    if filename is not None:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        os.remove(file_path)
    return 'deleted'


@app.route('/input/<filename>')
def send_image_input(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route('/output/<filename>')
def send_image_output(filename):
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename.replace('jpg', 'png'))


if __name__ == "__main__":
    eval.load_model()
    app.run(debug=True, port=5000)
