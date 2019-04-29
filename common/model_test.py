from keras.models import load_model
import cv2
import numpy as np


# settings
UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])


def model_test():
	model = load_model('full_retina_model.h5')
	# model.compile(loss='binary_crossentropy',
	#               optimizer='rmsprop',
	#               metrics=['accuracy'])

	img = cv2.imread('images/test.jpg')
	# img = cv2.resize(img,(320,240))
	# img = np.reshape(img,[1,320,240,3])

	classes = model.predict_classes(img)
	print (classes)

	return classes


# fun to check the file type
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
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
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)