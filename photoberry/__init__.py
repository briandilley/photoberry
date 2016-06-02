from flask import Flask, render_template

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

