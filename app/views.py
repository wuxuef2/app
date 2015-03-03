from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
import os
from flask import Flask, request, redirect, url_for
from flask import json, jsonify
from werkzeug import secure_filename
import random
from PIL import Image
import cv2
import numpy as np
import ctypes

# index view function suppressed for brevity

'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
        title = 'Sign In',
        form = form)
'''

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
            img = Image.open(app.config['UPLOAD_FOLDER'] + '/' + filename)
            
            width = img.size[0]
            height = img.size[1]
            pdll = ctypes.CDLL("./wuxuef.so")
            pdll.getShape.restype = ctypes.POINTER(ctypes.c_double * 136)
            points = []
            points = pdll.getShape("input.jpg", "1").contents
            print (len(points))
            print points[0:136]
            pointX = []     
            pointY = []
                         
            for i in range(0, 68):
                pointX[i] = points[i * 2]
                pointY[i] = points[i * 2 + 1]          

            return jsonify(path = filename, 
                            width = img.size[0], 
                            height = img.size[1],
                            pointX = pointX,
                            pointY = pointY,
                            pointSize = 68)
            
    return render_template('upload.html')
    
