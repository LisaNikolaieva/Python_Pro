import datetime
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from celery_worker import task1
import sqlite3






UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




# @app.route('/')
# def hello_world():  # put application's code here
#     task_obj = task1.apply_async(args=[str(uuid.uuid4())])
#     return str(task_obj)



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
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            task_obj = task1.apply_async(args=[filepath])
            con = sqlite3.connect("db1.db")
            cur = con.cursor()
            cur.execute(f"INSERT INTO task_state (datetime, file_name, status) VALUES ('{datetime.datetime.now()}','{filepath}','Added') ")
            con.commit()
            con.close()
            return str(task_obj)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''




if __name__ == '__main__':
    app.run()
