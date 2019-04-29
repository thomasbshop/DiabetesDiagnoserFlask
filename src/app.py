from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

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

# post the image.
@app.route('/image', methods=['POST'])
def add_image():
	image_name = request.json['image_name']
	description = request.json['description']


	new_image = RetinaImage(image_name, description)

	db.session.add(new_image)
	db.session.commit()

	return image_schema.jsonify(new_image)

# run server
if __name__ == '__main__':
	app.run(debug=True)