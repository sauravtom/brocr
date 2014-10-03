#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask, flask.views
app = flask.Flask(__name__)
from flask import render_template,request,make_response,Response,send_from_directory,redirect

import json,datetime,os,hashlib,datetime
import base64

import expeval
from expeval import dothings
from PIL import Image
import pytesseract
##

def image_to_text(img_data):
    #to correct padding in the base64_string
    img_data += "=" * ((4 - len(img_data) % 4) % 4)
    img_data = img_data.replace('data:image/png;base64,','')
    binary_data = base64.b64decode(img_data)
    fd = open('image.png', 'wb')
    fd.write(binary_data)
    fd.close()
    text = pytesseract.image_to_string(Image.open('image.png'))
    return text

@app.route('/analyze', methods=['POST'])
def analyze():
    text = image_to_text(request.form['imgBase64'])
    if not text:
        text = "Could not identify the image."
    else:
        flag=0
        for tex in text:
            if ord(tex)>57 or ord(tex)<32:
                flag=1
        if flag!=1:
            text=text+'='+dothings(text)
    return text

@app.route('/')
def demo():
    return flask.render_template('index.html')

if __name__ == '__main__':
    #app.jinja_env.filters['image_to_text'] = image_to_text
    app.debug = True
    app.run(host='0.0.0.0')

