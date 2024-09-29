from flask import Flask, render_template, request, send_file
import string
import random
import utils
import os
from PIL import Image
import jsonify
import logging



app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

window_height = 700
height_adjust = 70
image_suffixes = ("jpg", "jpeg", "gif", "webp")
video_suffixes = ("mp4", "webm")
# app = Flask(__name__, static_url_path="", static_folder="templates")
g_current_path = "/"
g_file_list = []
g_loop_time = 5
g_current_file = ""
g_last_played = ""

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
    request_path = request.args.get('current_path')
    index = request_path.rfind("/")+1
    file_name = request_path[index:].replace(" ","_").replace(".","_")
    return play_file_return(request_path, file_name)

@app.route("/next_file")
def play_next_file():
    global g_file_list
    global g_current_file
    if g_current_file != "":
        next_file = utils.find_next_item(g_file_list, g_current_file)    
    else: # PLAY the first file if exists
        next_file = utils.get_first_playable_item(g_file_list)
    
    if next_file is None:
        return "Watch this space ... "
    else:
        return play_file_return(next_file['path'], next_file['id'])

@app.route("/previous_file")
def play_previous_file():
    global g_file_list
    global g_last_played, g_current_file
    if g_last_played != "":
        previous_file = utils.find_previous_item(g_file_list, g_current_file)
        return play_file_return(previous_file['path'], previous_file['id'])
    else:
        return "Watch this space ... "

def play_file_return(request_path, file_id):
    global g_current_file
    global window_height
    global g_loop_time
    global g_last_played

    if (g_last_played == ""):
        g_last_played = file_id
    else: 
        g_last_played = g_current_file

    g_current_file = file_id
    if request_path.endswith(image_suffixes):
        img = Image.open(request_path) 
        # check if it is an image or video
        return render_template("showimage.html", image=request_path, height=window_height, file_name=file_id, loop_time=g_loop_time)
    elif request_path.endswith(video_suffixes):
        return render_template("playvideo.html", image=request_path, height=window_height, file_name=file_id, loop_time=g_loop_time)
    else:
        abort(404)

@app.route("/update_height", methods=['POST'])
def update_height():
    global window_height
    height = request.json['height']
    window_height = height - height_adjust
    return "{result: True}"

@app.route("/loop_time", methods=['POST','GET'])
def loop_time():
    global g_loop_time
    if request.method == 'POST':
        form_loop_time = request.values.get('loop_time')
        g_loop_time = form_loop_time
    return render_template("loop_time.html", loop_time = g_loop_time)

@app.route("/file_listing", methods=['POST','GET'])
def get_file_listing():
    global g_current_path
    global g_file_list
    global g_loop_time
    filter_str = ""
    if request.method == 'POST':
        filter_str = request.values.get('filter')
        current_path = g_current_path
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
    g_current_path = current_path
    
    files = utils.list_files(current_path, filter_str)
    g_file_list = files
    return render_template("listing.html", files=files, loop_time = g_loop_time, current_path=current_path, parent_path=parent_path, filter_str=filter_str)

if __name__ == "__main__":
    app.run(debug=True)