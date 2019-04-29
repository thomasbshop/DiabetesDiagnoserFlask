from flask import Flask, flash, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# settings
UPLOAD_FOLDER = 'DiabetesFlaskApp/images'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# session
app.secret_key = 'thesecretkey'
app.config['SESSION_TYPE'] = 'filesystem'

# upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db / init sqlachemy
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)

# Image Class/Model
class RetinaImage(db.Model):
	"""Details needed with the image to be stored in the db"""
	image_id = db.Column(db.Integer, primary_key=True)
	image_name = db.Column(db.String(100)) #, unique=True
	description = db.Column(db.String(400))
	# image = db.Column(db.Image)

	def __init__(self, image_name, description):
		# self.image = image
		self.image_name = image_name
		self.description = description


# model schema
class RetinaImageSchema(ma.Schema):
	"""docstring for RetinaImageSchema"""
	class Meta:
		fields = ('image_id', 'image_name', 'description')

# init schema
image_schema = RetinaImageSchema(strict=True)
images_schema = RetinaImageSchema(many=True, strict=True)


# fun to check the file type
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# post the image.
@app.route('/upload', methods=['GET', 'POST'])
def add_image():
	if request.method == 'POST':
		# image_name = request.json['image_name']
		# description = request.json['description']


		# check if the post request has the file part
	    if 'file' not in request.files:
	        flash('No file part')
	        return redirect(request.url)
	    file = request.files['image']
	    # if user does not select file, browser also
	    # submit an empty part without filename
	    if file.filename == '':
	        flash('No selected file')
	        return redirect(request.url)
	    if file and allowed_file(file.filename):
	        filename = secure_filename(file.filename)
	        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	        the_image = uploaded_file(filename)
	        print(the_image)
	        return the_image


		# new_image = RetinaImage(image_name, description)

		# db.session.add(new_image)
		# db.session.commit()

		# return image_schema.jsonify(new_image)

# run server
if __name__ == '__main__':
	app.run(debug=True)