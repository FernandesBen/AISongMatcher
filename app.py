from flask import Flask, render_template, request
from controller.businesslogic import businesslogic
import numpy, cv2

app = Flask(__name__)

@app.route('/')
def home():
	return render_template("Home.html")

@app.route('/photo')
def photo():
    return render_template("Photo.html")

@app.route('/song')
def song():
    return render_template("Song.html")

@app.route('/controller', methods=['POST'])
def controller():
    if(request.method=='POST'):
        filestr = request.files['profile_pic'].read()
        npimg = numpy.frombuffer(filestr, dtype='int8')
        img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
        songFile = businesslogic(img)
    return render_template("Song.html", songFile = songFile)

if __name__ == '__main__':
	app.run(debug=True)
