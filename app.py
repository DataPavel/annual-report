from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

import pandas as pd
import boto3

from dotenv import load_dotenv

def configure():
    load_dotenv()

configure()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = ['csv', 'xlsx', 'xls']

# Create the low level functional client

client = boto3.client(
    's3',
    aws_access_key_id = os.getenv('aws_access_key_id'), 
    aws_secret_access_key = os.getenv('aws_secret_access_key'),
    region_name = os.getenv('region_name')
)
bucket = os.getenv('bucket')
class UploadFile(FlaskForm):
    upload = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
columns = ['Date', 'Company', 'Studio', 'Project', 'Category', 'Country',
       'Country_code', 'OS', 'Counterparty', 'Amount_USD']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/', methods=['GET',"POST"])
def upload():
    form = UploadFile()
    if form.validate_on_submit():
        # Save file to the upload folder
        file = form.upload.data
        if allowed_file(file.filename):
            file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                app.config['UPLOAD_FOLDER'],
                secure_filename(file.filename))
            file.save(file_path)
            if (len(pd.read_csv(file_path).columns) == len(columns))\
            and (pd.read_csv(file_path).columns == columns).mean():
                #Upload file to S3
                client.upload_file(file_path, bucket, file.filename)
                # Delete file from upload folder
                os.remove(file_path)
                flash('The file has been uploaded')
                return render_template('upload.html', form=form)
            else:
                # Delete file from upload folder
                os.remove(file_path)
                flash('Please check the column names')
                return render_template('upload.html', form=form)
            
        else:
            flash('Make sure you upload file in csv or xlsx format')
            return render_template('upload.html', form=form)
    return render_template('upload.html', form=form)