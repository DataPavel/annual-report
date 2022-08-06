from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

import pandas as pd
import csv




# Create a Flask Instance
app = Flask(__name__)



# Create a Sectet Key
app.config['SECRET_KEY'] = 'KEY'

# Create a Upload Form
class UploadForm(FlaskForm):
	upload = FileField('Upload')
	submit = SubmitField('Submit')



@app.route('/', methods=['GET', 'POST'])
def test():
	form = UploadForm()
	return render_template('test.html', form=form)

@app.route('/data', methods=['GET', 'POST'])
def data():
	if request.method == 'POST':
		file = request.form['upload']
#		df = list()
#		with open(file) as file:
#			csvfile = csv.reader(file)
#			for row in csvfile:
#				df.append(row)
		df = pd.read_csv(file)
		return render_template('data.html', df=df)
