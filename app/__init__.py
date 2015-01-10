from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

UPLOAD_FOLDER = 'app/static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

from app import views


