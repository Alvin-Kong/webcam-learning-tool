# from flask import Flask, render_template, request
# from werkzeug.utils import secure_filename
# app = Flask(__name__)

# # @app.route('/')
# # def upload_file():
# #    return render_template('upload.html')
	
# @app.route('/', methods = ['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       return 'file uploaded successfully'
		
# if __name__ == '__main__':
#    app.run(debug = True)



# from flask import Flask, render_template, request
# from flask_cors import CORS
# from werkzeug.utils import secure_filename
# import os

# app = Flask(__name__)
# cors = CORS(app)

# @app.route('/form')
# def form():
#     return render_template('form.html')


# @app.route("/upload", methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         f = request.files.get('file')
#         full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'resume1')
#         f.save(full_filename)



#         return ("Uploaded Successfully")

# if __name__ == '__main__':
#    app.run(debug = False)



import os
import json
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/alvin/Desktop'
ALLOWED_EXTENSIONS = {'png','jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print("request: ", request)
        print("request.files: ", request.files)
        # if 'file' not in request.files:
        #     print('No file part')
        #     return redirect(request.url)
        # file = request.files['file']
        # # If the user does not select a file, the browser submits an
        # # empty file without a filename.
        # if file.filename == '':
        #     print('No selected file')
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     print(filename)
        #     print(os.path.join(app.config['UPLOAD_FOLDER']))
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     return redirect(url_for('download_file', name=filename))

        if "file" in request.files:
            file = request.files["file"]
            print("file: ", file)
            # if file.filename == '':
            #     print("ERROR: no selected file")
            #     return redirect(request.url)
            # elif file and allowed_file(file.filename):
            #     filename = secure_filename(file.filename)
            #     print(filename)
            #     print(os.path.join(app.config['UPLOAD_FOLDER']))
            #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #     return redirect(url_for('download_file', name=filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "canvas-image.png"))
            return redirect(url_for('download_file', name="canvas-image.png"))
        else:
            print("ERROR: no file in request query")
            return json.dumps("no file detected"), {"Content-Type": "application/json"}

    return


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == '__main__':
    PORT = 5000  # port to run the server on
    DEBUG = False  # whether to run in debug mode
    SSL_CONTEXT = None  # indicates whether to use HTTPS
    app.config["DEBUG"] = False
    app.run(port=PORT, ssl_context=SSL_CONTEXT)
