
from flask import Flask, Response, render_template

from photoberry.camera import controller

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def start_screen():
    return render_template('start.html')

@app.route('/take-photos')
def take_photos():
    return render_template('take_photos.html')

@app.route('/done')
def done():
    return render_template('done.html')

@app.route('/video-feed')
def video_feed():

    def _gen_photo_frames():
        while True:
            frame = controller.read_photo_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.getvalue() + b'\r\n')

    return Response(_gen_photo_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
