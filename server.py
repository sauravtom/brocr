#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask, flask.views
app = flask.Flask(__name__)
from flask import render_template,request,make_response,Response,send_from_directory,redirect

import json,datetime,os,hashlib,datetime
from binascii import a2b_base64
import base64

import Image
import pytesseract

def image_to_text(img_data):
    print img_data
    #ugly hack to avoid a terrible jinja template error
    if 'ZWDJXlYAAAAASUVORK5CYII=' in img_data < 10:
        return 0;
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
    return text

@app.route('/')
def demo():
    return flask.render_template('index.html')

if __name__ == '__main__':
    #analyze_image("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAfQAAABkCAYAAABwx8J9AAAHRklEQVR4Xu3dTXIbRRgGYIcFFCtgwzmAC+ElO+Am5AbmROEebJIVVWySHpBAUc3op+dVPk3rcZUrCXZ/3/QzLb/q0ci8evJBgAABAgQIbF7g1eZnYAIECBAgQIDAk0C3CAgQIECAwAACAn2Ak2gKBAgQIEBAoFsDBAgQIEBgAAGBPsBJNAUCBAgQICDQrQECBAgQIDCAgEAf4CSaAgECBAgQEOjWAAECBAgQGEBAoA9wEk2BAAECBAgIdGuAAAECBAgMICDQBziJpkCAAAECBAS6NUCAAAECBAYQEOgDnERTIECAAAECAt0aIECAAAECAwgI9AFOoikQIECAAAGBbg0QIECAAIEBBO4q0N8/Pf3WTH9sn1/ubP9qf760g/x1AGtTIECAAAECNxO4m0DfhfnPCzN93Q70l5spKEyAAAECBDYucE+B/rZZfrXg2fL+aQp1O/WNLziHT4AAAQK3EdhKoO9nb6d+m3WgKgECBAhsXOCeAn16/XzpkvueedrF/94+p9fZpw+vr298ATp8AgQIEMgI3E2gT9PZvY7+3P463RT3+cwU/57573btmbWgCgECBAhsWOCuAv3QceEmublAt2vf8AJ8tEPfreuf2ry/2M19uj/k8HH4pv3jh0dzMV8CBNYL3G2gH+3Yp3++tM9p935845xd+/p1oMKNBWaC/FTHP9oD8/sbH5LyBAgMJnDXgX5sfc2uvU3sm/34g/e3//PEwN3yg63iO5rO3Fo785bMuaN/39boZ3c0LYdCgMAGBDYV6Ffs2t+1iX198P3HN9t53X0Di3Nrh7gQ3K8XriydnF5bv5t7bG7tfDleAqMJbP6HxtIP0f0vomlfn3t/+9vDHfzClQB30o+22gPzOXW1Z2mttbbT42zpdyzMHZVL7oFzpQSBRxPYfKDP7doPf6vcwg/Z/3bwC2FuR/9oj4QL5tv55PFdK/3SPs+9JXN/BH+29fvtBYfjWwgQIPCRwBCBfuqcnvshPBPoV+/oranHEDh3tefUWmtfe9OUvjuSmi7HTx/Puz+n+zv8iuPHWE5mSSAuMHygn9vBXxjoizv6pTPiRrz4Wi0veMnVnoPfpTAd70cBfepr5ZNzAAQIbF7gIQL9mrN07Y5+rvbaGr1PBnrG9Yw5nHPl+N7eK8d5OeaaB5TvJUDgkwkI9BnqtTupc5dmT53d3icDPeN6xsyEeXfArenfO7Z33H7ea9fGJ3tka0SAwMMJCPQbnPJLLs2euFTf9Rp+z5OInjFHgd51rAfh2D2+99h7x91gmShJgACBqIBAj3L+W2zNLrD3yUDPuJ4xFwT6xfcbrOnfO7Z33A2WiZIECBCICgj0KOf/xXovzfY+GegZ1zPm0S+532i5KEuAAIHVAgJ9NWG+wMonA8+7I7roLVC9vQ4um0//29ures48Kega33vsvePyZ1pFAgQI5AQEes5SJQIECBAgUCYg0MvoNSZAgAABAjkBgZ6zVIkAAQIECJQJCPQyeo0JECBAgEBOQKDnLFUiQIAAAQJlAgK9jF5jAgQIECCQExDoOUuVCBAgQIBAmYBAL6PXmAABAgQI5AQEes5SJQIECBAgUCYg0MvoNSZAgAABAjkBgZ6zVIkAAQIECJQJCPQyeo0JECBAgEBOQKDnLFUiQIAAAQJlAgK9jF5jAgQIECCQExDoOUuVCBAgQIBAmYBAL6PXmAABAgQI5AQEes5SJQIECBAgUCYg0MvoNSZAgAABAjkBgZ6zVIkAAQIECJQJCPQyeo0JECBAgEBOQKDnLFUiQIAAAQJlAgK9jF5jAgQIECCQExDoOUuVCBAgQIBAmYBAL6PXmAABAgQI5AQEes5SJQIECBAgUCYg0MvoNSZAgAABAjkBgZ6zVIkAAQIECJQJCPQyeo0JECBAgEBOQKDnLFUiQIAAAQJlAgK9jF5jAgQIECCQExDoOUuVCBAgQIBAmYBAL6PXmAABAgQI5AQEes5SJQIECBAgUCYg0MvoNSZAgAABAjkBgZ6zVIkAAQIECJQJCPQyeo0JECBAgEBOQKDnLFUiQIAAAQJlAgK9jF5jAgQIECCQExDoOUuVCBAgQIBAmYBAL6PXmAABAgQI5AQEes5SJQIECBAgUCYg0MvoNSZAgAABAjkBgZ6zVIkAAQIECJQJCPQyeo0JECBAgEBOQKDnLFUiQIAAAQJlAgK9jF5jAgQIECCQExDoOUuVCBAgQIBAmYBAL6PXmAABAgQI5AQEes5SJQIECBAgUCYg0MvoNSZAgAABAjkBgZ6zVIkAAQIECJQJCPQyeo0JECBAgEBOQKDnLFUiQIAAAQJlAgK9jF5jAgQIECCQExDoOUuVCBAgQIBAmYBAL6PXmAABAgQI5AQEes5SJQIECBAgUCYg0MvoNSZAgAABAjkBgZ6zVIkAAQIECJQJCPQyeo0JECBAgEBOQKDnLFUiQIAAAQJlAgK9jF5jAgQIECCQExDoOUuVCBAgQIBAmcAHAaMcdGU0U0gAAAAASUVORK5CYII=")
    #app.jinja_env.filters['image_to_text'] = image_to_text
    app.debug = True
    app.run(host='0.0.0.0')

