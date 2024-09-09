from flask import Flask, request, redirect, jsonify, render_template
import threading
import time

import createcolmap as createcolmap
import imagesfromvid as imagesfromvid
import rerun_test as rerun_test
import run_rerun as run_rerun

app = Flask(__name__)

rerun_started = False
uploaded_video_filename = None

def start_rerun():
    global rerun_started
    run_rerun.run()
    rerun_started = True

def stop_rerun_after_delay():
    time.sleep(5)
    if rerun_started:
        print("Stopping Rerun...")

@app.route('/start-rerun', methods=['POST'])
def start_rerun_endpoint():
    global rerun_started
    rerun_started = False
    rerun_thread = threading.Thread(target=start_rerun)
    rerun_thread.start()

    stop_thread = threading.Thread(target=stop_rerun_after_delay)
    stop_thread.start()

@app.route('/')
def index():
    return render_template('webpage.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    result = imagesfromvid.create_images('vid.mp4') # base other variables: n_images = 5, n_same_images = 1, frametake = 10
    createcolmap.run() # base other variables: image_dir = 'images', database_path = "database.db", sparse_dir = "sparse", colmap_executable = r"C:\Users\noahv\Downloads\colmap-x64-windows-nocuda\COLMAP.bat"
    run_rerun.run()
    rerun_test.run()
    return jsonify(result=result)

@app.route('/upload', methods=['POST'])
def upload():
    global uploaded_video_filename

    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and file.filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        uploaded_video_filename = file.filename
        file.save(f'./uploads/{file.filename}')
        return f'File uploaded successfully: {file.filename}'
    
    return 'Invalid file type'

if __name__ == '__main__':
    app.run(debug=True)