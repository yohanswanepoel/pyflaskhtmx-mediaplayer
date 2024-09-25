from flask import Flask, render_template, request, send_file
import string
import random
import utils
import os
from PIL import Image
import jsonify
import logging



app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

window_height = 700
image_suffixes = ("jpg", "jpeg", "gif", "webp")
video_suffixes = ("mp4", "webm")
# app = Flask(__name__, static_url_path="", static_folder="templates")
global_current_path = "/"

@app.route("/")
def index():
    global window_height
    return render_template("index.html", height=window_height)

@app.route("/send_image")
def send_image():
    request_path = request.args.get('filename')
    if os.path.isfile(request_path):
        return send_file(request_path)
    else:
        abort(404)  #
    return request_path

@app.route("/play_file")
def play_current_file():
    global window_height
    request_path = request.args.get('current_path')
    index = request_path.rfind("/")+1
    file_name = request_path[index:].replace(" ","_").replace(".","_")
    if request_path.endswith(image_suffixes):
        img = Image.open(request_path) 
        # check if it is an image or video
        return render_template("showimage.html", image=request_path, height=window_height, file_name=file_name)
    elif request_path.endswith(video_suffixes):
        return render_template("playvideo.html", image=request_path, height=window_height, file_name=file_name)
    else:
        abort(404)

@app.route("/update_height", methods=['POST'])
def update_height():
    global window_height
    height = request.json['height']
    window_height = height - 100
    return "{result: True}"

@app.route("/file_listing", methods=['POST','GET'])
def get_file_listing():
    global global_current_path
    filter_str = ""
    if request.method == 'POST':
        filter_str = request.values.get('filter')
        current_path = global_current_path
    else:  # GET Method Code
        request_path = request.args.get('current_path')
        parent_path = "/"

        if request_path is None:
            current_path = utils.get_curent_path()
        else:
            current_path = request_path

    parent_path = current_path[0:current_path.rfind("/")]
    if current_path == "/":
        parent_path = "/"
    else:
        parent_path = current_path[0:current_path.rfind("/")]
    if parent_path == "":
        parent_path = "/"
    current_path = current_path.replace("//","/")
    global_current_path = current_path
    
    files = utils.list_files(current_path, filter_str)
    return render_template("listing.html", files=files, current_path=current_path, parent_path=parent_path, filter_str=filter_str)

if __name__ == "__main__":
    app.run(debug=True)