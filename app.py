import os
from flask import Flask, flash, jsonify, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# custom
import config
import models

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# port
port = int(os.getenv("PORT", 9099))

# session
app.secret_key = 'thesecretkey'
app.config['SESSION_TYPE'] = 'filesystem'

# upload folder
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
# UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'imageprofiles.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db / init sqlachemy
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)


# fun to check the file type
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("home.html")


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)

# post the image.
@app.route('/api/upload', methods=['GET', 'POST'])
def add_profile():
	if request.method == 'POST':
		# check if the post request has the file part
	    if 'image' not in request.files:
	        flash('No file part')
	        # return redirect(request.url)
	        return jsonify({"description":"no file part"})
	        
	    file = request.files['image']
	    # if user does not select file, browser also
	    # submit an empty part without filename
	    if file.filename == '':
	        flash('No selected file')
	        # return redirect(request.url)
	        return jsonify({"description":"no selected file"})

	    if file and allowed_file(file.filename):
	        filename = secure_filename(file.filename)
	        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	        # data
	        lname = request.form['lastname']
	        fname = request.form['firstname']
	        results = request.form['results']
	        description = request.form['description']
	        image_name = filename

	        new_profile = models.ImageProfile(lname, fname, image_name, results, description)

	        config.db.session.add(new_profile)
	        config.db.session.commit()

	        return models.image_schema.jsonify(new_profile)
	        # return redirect(url_for('uploaded_file', filename=filename))
	    else:
	    	print("That file extension is not allowed")
	    	return redirect(request.url)

	return render_template("upload.html")


		# return image_schema.jsonify(new_profile)

# run server
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)