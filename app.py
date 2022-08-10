from flask import Flask, render_template, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, DateField, SelectMultipleField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired, DataRequired

import plotly
import json

import pandas as pd
import numpy as np

import utils
import plots

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'


class UploadFile(FlaskForm):
    upload = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/', methods=['GET',"POST"])
def upload():
    form = UploadFile()
    if form.validate_on_submit():
        # Save file to the upload folder
        file = form.upload.data
        if utils.allowed_file(file.filename):
            file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                app.config['UPLOAD_FOLDER'],
                secure_filename(file.filename))
            file.save(file_path)
            if (len(pd.read_csv(file_path).columns) == len(utils.columns))\
            and (pd.read_csv(file_path).columns == utils.columns).mean():
                #Upload file to S3
                utils.client.upload_file(file_path, utils.bucket, file.filename)
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

class FilterForm(FlaskForm):

    start_date = DateField('Start Date')
    end_date = DateField('End Date')
    company_name = SelectMultipleField('Company Name',
        validate_choice=False)
    studio_name = SelectMultipleField('Studio', choices=[],
        validate_choice=False)
    product_name = SelectMultipleField('Product', choices=[],
        validate_choice=False)
    submit = SubmitField('Submit')

df = utils.read_file_s3().groupby('Date').sum()['Amount_USD'].reset_index()
df['color'] = np.where(df['Amount_USD']<0, '#F43B76', '#36CE53')
df['RT'] = df['Amount_USD'].cumsum()
df['color_RT'] = np.where(df['RT']<0, '#F43B76', '#36CE53')
df_project = utils.read_file_s3().groupby('Project').sum()['Amount_USD'].reset_index()
df_project['color'] = np.where(df_project['Amount_USD']<0, '#F43B76', '#36CE53')

@app.route('/profit/')
def profit():
    form = FilterForm()
    form.company_name.choices=['All'] + utils.unique_value('Company')
    form.studio_name.choices=['All']+ utils.unique_value('Studio')
    form.product_name.choices=['All']+ utils.unique_value('Project')

    fig = plots.profit_by_month_bar(df)
    graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    fig2 = plots.cumline(df)
    graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    fig3 = plots.bar_project(df_project)
    graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('profit.html', form=form, graph=graph, graph2=graph2, graph3=graph3)










### TODO
# https://www.youtube.com/watch?v=I2dJuNwlIH0
# Dynamic Select Fields
@app.route('/studio/<company>')
def studio(company):
    df = utils.read_file_s3()
    studios = list(df[df['Company']==company]['Studio'].unique())
    studioArray = list()
    for studio in studios:
        studioObj = {}
        studioObj['id'] = studio
        studioObj['name'] = studio
        studioArray.append(studioObj)
    return jsonify( {'studios': studioArray})



