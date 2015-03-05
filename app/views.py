from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
import os
from flask import Flask, request, redirect, url_for
from flask import json, jsonify
from werkzeug import secure_filename
import random
from PIL import Image
import ctypes
import time

# index view function suppressed for brevity

ALLOWED_EXTENSIONS = set(['bmp', 'BMP', 'tif', 'TIF', 'tiff', 'TIFF', 'png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'gif', 'GIF'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        #curAge = request.files['curAge']
                
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imagePath = app.config['UPLOAD_FOLDER'] + '/' + filename
            img = Image.open(imagePath)
            
            width = img.size[0]
            height = img.size[1]
            pdll = ctypes.CDLL("./wuxuef.so")
            pdll.getShape.restype = ctypes.POINTER(ctypes.c_double * 136)
            points = []
            
            points = pdll.getShape(imagePath, "1").contents
            print (len(points))
            print points[0:136]
            pointX = []     
            pointY = []
                         
            for i in range(0, 68):
                pointX.append(points[i * 2])
                pointY.append(points[i * 2 + 1])          

            return jsonify(path = filename, 
                            width = img.size[0], 
                            height = img.size[1],
                            pointX = pointX,
                            pointY = pointY,
                            pointSize = 68)
            
    return render_template('upload.html')
    

@app.route('/age', methods=['POST'])
def age():
    imagePath = request.form['image']
    curAge = request.form['curAging']
    forecastAge = request.form['forecastAge']
    points = request.form['points']
     
    pdll = ctypes.CDLL("./wuxuef.so")
    pdll.fit.argtypes = [ctypes.c_char_p, 
                         ctypes.c_char_p, 
                         ctypes.c_char_p, 
                         ctypes.c_char_p, 
                         ctypes.c_int]
    
    image = app.config['UPLOAD_FOLDER'] + '/' + imagePath
    print image
    code = pdll.fit(image, curAge, forecastAge, points, 136)
    return jsonify(code = code)
