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
import string

# index view function suppressed for brevity

ALLOWED_EXTENSIONS = set(['bmp', 'BMP', 'tif', 'TIF', 'tiff', 'TIFF', 'png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'gif', 'GIF'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def package(code, mess, data):
    return jsonify(code = code,
                   mess = mess,
                   data = data)
ERROR_MESSAGE = ["Normal",                      #0
                 "Cannot Read Uploaded Image",  #1
                 "Not Find Face",               #2
                 "System Busy",                 #3
                 "Age Input Error",             #4
                 "Shapes != Images",            #5
                 "Age error!",                  #6
                 "The image channels must be 3, and the depth must be 8!"]#7    
           
def upload():
    file = request.files['file']
                
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagePath = app.config['UPLOAD_FOLDER'] + '/' + filename
        ticks = repr(time.time())
        
        
        os.renames(imagePath, app.config['UPLOAD_FOLDER'] + '/' + ticks + filename)
        filename = ticks + filename
        imagePath = app.config['UPLOAD_FOLDER'] + '/' + filename
        
        try:
            img = Image.open(imagePath)
        except:
            return package(-1, "App couldn't understand the upload file.", {})
        
        width = img.size[0]
        height = img.size[1]
        pdll = ctypes.CDLL("./wuxuef.so")
        pdll.getShape.restype = ctypes.POINTER(ctypes.c_double * 137)
        points = []
        
        points = pdll.getShape(imagePath, "1").contents


        pointX = []     
        pointY = []
        
        curAge = int(points[68 * 2])
        if curAge < 0:
            return package(-1, ERROR_MESSAGE[-curAge], {})
                     
        for i in range(0, 68):
            pointX.append(points[i * 2])
            pointY.append(points[i * 2 + 1])          

        return package(0, "", {'path' : filename, 
                        'width' : img.size[0], 
                        'height' : img.size[1],
                        'pointX' : pointX,
                        'pointY' : pointY,
                        'curAge' : points[68 * 2],
                        'pointSize' : 68})
    return package(-1, "App couldn't understand the upload file.", {})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return upload()
            
    return render_template('upload.html')

@app.route('/Help', methods=['GET'])
def support():          
    return render_template('Help.html')
    

@app.route('/age', methods=['POST'])
def age():
    imagePath = request.form['image']
    curAge = request.form['curAging']
    forecastAge = request.form['forecastAge']
    points = request.form['points']
    counter = request.form['times']
     
    pdll = ctypes.CDLL("./wuxuef.so")
    pdll.fit.argtypes = [ctypes.c_char_p, 
                         ctypes.c_char_p, 
                         ctypes.c_char_p, 
                         ctypes.c_char_p, 
                         ctypes.c_int,
                         ctypes.c_int]
    
    image = app.config['UPLOAD_FOLDER'] + '/' + imagePath
    newImage = 'result_' + counter + imagePath
    print(newImage)
    code = pdll.fit(image, curAge, forecastAge, points, 136, string.atoi(counter))
    return jsonify(code = code, newImage = newImage, curAge = curAge, forecastAge = forecastAge)

@app.route('/upload', methods=['POST'])
def uploadImage():
    return upload()
