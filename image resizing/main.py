from flask import Flask, request, render_template, send_from_directory
from PIL import Image
import os

app = Flask(__name__)

# Set the directory where uploaded images are stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return render_template('upload.html', msg='No file selected')

    file = request.files['file']

    if file.filename == '':
        return render_template('upload.html', msg='No file selected')

    if file and allowed_file(file.filename):
        width = request.form['width']
        height = request.form['height']

        # Open the image and resize it
        im = Image.open(file)
        im = im.resize((int(width), int(height)))

        # Save the resized image to a temporary file
        temp_file = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        im.save(temp_file)

        return render_template('view.html', image=file.filename)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run()
