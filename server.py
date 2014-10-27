#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask, flask.views
app = flask.Flask(__name__)
from flask import render_template,request,make_response,Response,send_from_directory,redirect

import json,datetime,os,hashlib,datetime
import base64

import expeval
from expeval import dothings
#import numpy
import cv2
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
    im2=cv2.imread('image.png')
    im2=cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    im3 = cv2.adaptiveThreshold(blur,255,1,1,11,2)
    im=im3.copy()
    contours,hierarchy = cv2.findContours(im,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    text=''

    for cnt in contours:
        if cv2.contourArea(cnt)>30:
            [x,y,w,h] = cv2.boundingRect(cnt)
            bbox = (x, y, x+w, y+h)
            im1=im.crop(bbox)
            text = text + pytesseract.image_to_string(im1,'English',10,'True')
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

