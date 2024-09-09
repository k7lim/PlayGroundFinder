import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import logging

# Add this near the top of your file
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads/')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.chmod(app.config['UPLOAD_FOLDER'], 0o755)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        logging.debug("POST request received")
        if 'file' not in request.files:
            logging.debug("No file part in the request")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            logging.debug("No file selected")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            logging.debug(f"Saving file to: {filepath}")
            file.save(filepath)
            logging.debug(f"File saved successfully")
            return f'File {filename} uploaded successfully'
        else:
            logging.debug(f"File not allowed: {file.filename}")
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)