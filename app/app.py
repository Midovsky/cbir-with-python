# -*- coding:utf-8 -*-
import os
import sys
from flask import send_from_directory

from flask import Flask, render_template, request, jsonify, redirect, url_for
 
from search.colordescriptor import ColorDescriptor
from search.searcher import Searcher
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/midovsky/Desktop/test/app/static/queries'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# create flask instance
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

INDEX = os.path.join(os.path.dirname(__file__), 'index.csv')

fn=''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# main route
@app.route('/', methods=['GET'])
def index():

    files = os.listdir(app.config['UPLOAD_FOLDER'])

    return render_template('index.html',files=files)

@app.route('/', methods=['POST'])
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
            fn=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(fn)
            #return index()
            #return redirect(url_for('search', x=x, y=y))
            #search2(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('search2', xx=fn))
            return redirect(url_for('index'))


@app.route('/static/queries/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# search route
@app.route('/search', methods=['POST'])
def search():

    if request.method == "POST":
 
        RESULTS_ARRAY = []
 
        # get url
        image_url = request.form.get('img')

        try:

            # initialize the image descriptor
            cd = ColorDescriptor((8, 12, 3))
            # load the query image and describe it
            from skimage import io
            import cv2
            print(cv2.__version__)

            # query = io.imread(image_url)
            # query = (query * 255).astype("uint8")
            # (r, g, b) = cv2.split(query)
            # query = cv2.merge([b, g, r])
            print(image_url)

            image_url = "/home/midovsky/Desktop/test/app/" + image_url[1:]
            print(image_url)


            # print "图像url路径:", image_url
            # print os.getcwd()
            # print sys.path[0]
            query = cv2.imread(image_url)
                        
                        
            print(query)

            # print "读取成功！"
            features = cd.describe(query)

            # print "描述子生成成功"

            # perform the search
            searcher = Searcher(INDEX)
            results = searcher.search(features)

            # loop over the results, displaying the score and image name
            for (score, resultID) in results:
                RESULTS_ARRAY.append(
                    {"image": str(resultID), "score": str(score)})
 
            # return success
            return jsonify(results=(RESULTS_ARRAY[:10]))
 
        except:
 
            # return error
            return jsonify({"sorry": "Sorry, no results! Please try again."}), 500




@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('index.html', data = filename)


@app.route('/search2/<xx>', methods = ['POST'])
def search2(xx):
 
    if request.method == "POST":
        RESULTS_ARRAY = []

        try:
            # initialize the image descriptor
            cd = ColorDescriptor((8, 12, 3))

            # load the query image and describe it
            from skimage import io
            import cv2
            # query = io.imread(image_url)
            # query = (query * 255).astype("uint8")
            # (r, g, b) = cv2.split(query)
            # query = cv2.merge([b, g, r])

            image_url = xx
            # print "图像url路径:", image_url
            # print os.getcwd()
            # print sys.path[0]
            query = cv2.imread(image_url)
            # print "读取成功！"
            features = cd.describe(query)

            # print "描述子生成成功"

            # perform the search
            searcher = Searcher(INDEX)
            results = searcher.search(features)
            # loop over the results, displaying the score and image name
            for (score, resultID) in results:
                RESULTS_ARRAY.append(
                    {"image": str(resultID), "score": str(score)})

            # return success
            return jsonify(results=(RESULTS_ARRAY[:5]))

        except:

            # return error
            jsonify({"sorry": "Sorry, no results! Please try again."}), 500

# run!
if __name__ == '__main__':
    app.run('127.0.0.1', debug=True)
