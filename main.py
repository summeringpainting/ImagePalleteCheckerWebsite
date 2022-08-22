from flask import Flask, render_template, send_from_directory, url_for
import numpy as np
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from colorthief import ColorThief
import os


app = Flask(__name__)

# Create random secret key
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('Upload')

def determine_color_codes_for_image(image):
    """ Gets the most prominent colors in the image. """
    color_thief = ColorThief(image)
    try:
        return color_thief.get_palette()
    except:
        pass
    return []



@app.route('/get_colors/<filename>', methods=['GET', 'POST'])
def get_colors(filename):
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = "/uploads/IMG_7045.jpg"
    codes = determine_color_codes_for_image(f"uploads/{filename}")
    return render_template('index.html', form=form, file_url=file_url, filename=filename, codes=codes)

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = "/uploads/IMG_7045.jpg"
    return render_template('index.html', form=form, file_url=file_url, codes="(0,0,0)")



if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=5000)
