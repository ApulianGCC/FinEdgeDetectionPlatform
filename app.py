from flask import Flask, session, flash, request, redirect, render_template, send_from_directory, send_file
from flask_dropzone import Dropzone
import eval
import os
from werkzeug.utils import secure_filename
from zipfile import ZipFile


UPLOAD_FOLDER = 'input/'
OUTPUT_FOLDER = 'result/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")
app = Flask(__name__, static_url_path="/static", static_folder=static_file_dir)
app.secret_key = os.urandom(16)
dropzone = Dropzone(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_PARALLEL_UPLOADS'] = 10
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*, .jpg, .jpeg'
app.config['DROPZONE_MAX_FILE_SIZE'] = 16 * 1024 * 1024
app.config['DROPZONE_MAX_FILES'] = 10
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
        file_names=[]
        if session.get('file_name') is not None:
            for file in session.get('file_name'):
                file_names.append(file)
        for key, f in request.files.items():
            if key.startswith('file'):
                if f and allowed_file(f.filename):
                    filename = secure_filename(f.filename)
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'] + filename))
                    file_names.append(filename)
        session['file_name'] = file_names
        print(session)
        '''
        f = request.files.get('file')
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'] + filename))
            session['file_name'] = filename
        '''
    return 'uploaded'


@app.route('/get_outline')
def get_outline():

    file_name = session.get('file_name')
    print((file_name))
    if file_name is not None:
        eval.run(file_name)
        if len(file_name) == 1:
            return render_template("result.html", title="result", filename=file_name)
        else:
            return render_template("multiple_results.html", title="result", filename=file_name)
    else:
        flash('devi caricare una foto')

    return redirect(request.url)


@app.route('/cancel_upload', methods=['GET', 'POST'])
def cancel_upload():
    file_name = session.get('file_name')
    if file_name is not None:
        for file in file_name:
            file_path = os.path.join(UPLOAD_FOLDER, file)
            os.remove(file_path)
        session['file_name']=None
    return 'deleted'


@app.route('/input/<filename>')
def send_image_input(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route('/output/<filename>')
def send_image_output(filename):
    return send_from_directory(app.config["OUTPUT_FOLDER"], eval.change_extension(filename),  as_attachment=True)

@app.route('/zipdownloads')
def send_zip_output():
    zipObj = ZipFile(os.path.join(app.config["OUTPUT_FOLDER"], 'results.zip'), 'w')

    filename = session.get('file_name')

    for file in filename:
        print(file)
        zipObj.write(os.path.join(app.config["OUTPUT_FOLDER"], eval.change_extension(file)))

    zipObj.close()

    return send_file(zipObj, attachment_filename='result.zip', as_attachment=True)


@app.route('/res/<filename>')
def send_image_static(filename):
    return send_from_directory(os.path.join(static_file_dir, 'res'), filename,  as_attachment=True)

if __name__ == "__main__":
    eval.load_model()
    app.run(debug=True, port=5000)