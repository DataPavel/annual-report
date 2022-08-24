from flask import Flask, render_template, flash, jsonify, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, DateField, SelectField, SelectMultipleField, IntegerField, DecimalField
from werkzeug.utils import secure_filename
import os

from wtforms.validators import InputRequired, DataRequired
from babel.numbers import format_decimal

import jinja2

import plotly
import json

import pandas as pd
import numpy as np

import utils
import plots
import preds
import dataframes


# Decimal format for Jinja2
def FormatDecimal(value):
    return format_decimal(float(value), format='#,##0')
def FormatScore(value):
    return format_decimal(float(value), format='#,##0.##')

jinja2.filters.FILTERS['FormatDecimal'] = FormatDecimal
jinja2.filters.FILTERS['FormatScore'] = FormatScore





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

    start_date = DateField('Start Date', validators=[InputRequired()])
    end_date = DateField('End Date', validators=[InputRequired()])
    company_name = SelectMultipleField('Company Name',
        validate_choice=False, validators=[InputRequired()])
    studio_name = SelectMultipleField('Studio', choices=[],
        validate_choice=False, validators=[InputRequired()])
    product_name = SelectMultipleField('Product', choices=[],
        validate_choice=False, validators=[InputRequired()])
    submit = SubmitField('Submit')

 


















###########################Profit Page###############################################################




@app.route('/profit/', methods=['GET',"POST"])
def profit():
    form = FilterForm()
    form.company_name.choices=['All'] + utils.unique_value('Company')
    form.studio_name.choices=['All']+ utils.unique_value('Studio')
    form.product_name.choices=['All']+ utils.unique_value('Project')
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        company_name = form.company_name.data
        studio_name = form.studio_name.data
        product_name = form.product_name.data
        if company_name[0] == 'All' and studio_name[0] == 'All' and product_name[0] == 'All':

            df = dataframes.df_main(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")
            df_project = dataframes.df_project(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")
            df_table = dataframes.df_table(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")
            df_preds = dataframes.df_preds(start_date="'"+str(start_date)+"'")

            fig = plots.profit_by_month_bar(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.cumline(df)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.bar_project(df_project)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.predictions(df_preds)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('profit.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
                    graph4=graph4, df=df_table)

        if company_name[0] != 'All' and studio_name[0] == 'All' and product_name[0] == 'All':

            df = dataframes.df_main(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)
            df_project = dataframes.df_project(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)
            df_table = dataframes.df_table(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)
            df_preds = dataframes.df_preds(start_date="'"+str(start_date)+"'", company_name=company_name)
            
            fig = plots.profit_by_month_bar(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.cumline(df)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.bar_project(df_project)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.predictions(df_preds)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('profit.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
                    graph4=graph4, df=df_table)
           
        if company_name[0] == 'All' and studio_name[0] != 'All' and product_name[0] == 'All':

            df = dataframes.df_main(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)
            df_project = dataframes.df_project(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)
            df_table = dataframes.df_table(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)
            df_preds = dataframes.df_preds(start_date="'"+str(start_date)+"'", studio_name=studio_name)
            
            fig = plots.profit_by_month_bar(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.cumline(df)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.bar_project(df_project)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.predictions(df_preds)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('profit.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
                    graph4=graph4, df=df_table)

        if company_name[0] == 'All' and studio_name[0] == 'All' and product_name[0] != 'All':

            df = dataframes.df_main(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)
            df_project = dataframes.df_project(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)
            df_table = dataframes.df_table(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)
            df_preds = dataframes.df_preds(start_date="'"+str(start_date)+"'", product_name=product_name)
            
            fig = plots.profit_by_month_bar(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.cumline(df)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.bar_project(df_project)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.predictions(df_preds)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('profit.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
                    graph4=graph4, df=df_table)

        if company_name[0] != 'All' and studio_name[0] != 'All' and product_name[0] == 'All':

            df = dataframes.df_main(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)
            df_project = dataframes.df_project(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)
            df_table = dataframes.df_table(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)
            df_preds = dataframes.df_preds(start_date="'"+str(start_date)+"'", company_name=company_name, studio_name=studio_name)
            
            fig = plots.profit_by_month_bar(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.cumline(df)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.bar_project(df_project)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.predictions(df_preds)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('profit.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
                    graph4=graph4, df=df_table)


        if company_name[0] != 'All' and studio_name[0] == 'All' and product_name[0] != 'All':

            df = dataframes.df_main(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)
            df_project = dataframes.df_project(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)
            df_table = dataframes.df_table(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)
            df_preds = dataframes.df_preds(start_date="'"+str(start_date)+"'", company_name=company_name, product_name=product_name)
            
            fig = plots.profit_by_month_bar(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.cumline(df)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.bar_project(df_project)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.predictions(df_preds)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('profit.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
                    graph4=graph4, df=df_table)


        if company_name[0] == 'All' and studio_name[0] != 'All' and product_name[0] != 'All':

            df = dataframes.df_main(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)
            df_project = dataframes.df_project(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)
            df_table = dataframes.df_table(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)
            df_preds = dataframes.df_preds(start_date="'"+str(start_date)+"'", studio_name=studio_name, product_name=product_name)
            
            fig = plots.profit_by_month_bar(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.cumline(df)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.bar_project(df_project)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.predictions(df_preds)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('profit.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
                    graph4=graph4, df=df_table)

        if company_name[0] != 'All' and studio_name[0] != 'All' and product_name[0] != 'All':

            df = dataframes.df_main(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)
            df_project = dataframes.df_project(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)
            df_table = dataframes.df_table(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)
            df_preds = dataframes.df_preds(start_date="'"+str(start_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)

            fig = plots.profit_by_month_bar(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.cumline(df)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.bar_project(df_project)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.predictions(df_preds)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('profit.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
                    graph4=graph4, df=df_table)

    df = dataframes.df_main_nf()
    df_project = dataframes.df_project_nf()
    df_table = dataframes.df_table_nf()
    df_preds = dataframes.df_preds_nf()
     
    fig = plots.profit_by_month_bar(df)
    graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    fig2 = plots.cumline(df)
    graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    fig3 = plots.bar_project(df_project)
    graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    fig4 = plots.predictions(df_preds)
    graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

    
    return render_template('profit.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
        graph4=graph4, df=df_table)























####################################Revenue Page########################################



@app.route('/revenue/', methods=['GET',"POST"])
def revenue():
    form = FilterForm()
    form.company_name.choices=['All'] + utils.unique_value('Company')
    form.studio_name.choices=['All']+ utils.unique_value('Studio')
    form.product_name.choices=['All']+ utils.unique_value('Project')
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        company_name = form.company_name.data
        studio_name = form.studio_name.data
        product_name = form.product_name.data
        if company_name[0] == 'All' and studio_name[0] == 'All' and product_name[0] == 'All':

            df = dataframes.df_revenue_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")
            df_country = dataframes.df_revenue_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")
            df_category = dataframes.df_revenue_category(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")
            df_partner1 = dataframes.df_revenue_partner1(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")
            df_partner2 = dataframes.df_revenue_partner2(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")
            df_table = dataframes.df_table_revenue(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")


            fig = plots.revenue_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.revenue_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_cat_rev(df_category)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.pie_partner_rev(df_partner1)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            fig5 = plots.pie_partner_rev(df_partner2)
            graph5=json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('revenue.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
                    graph4=graph4, graph5=graph5, df=df_table)

        if company_name[0] != 'All' and studio_name[0] == 'All' and product_name[0] == 'All':

            df = dataframes.df_revenue_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)
            df_country = dataframes.df_revenue_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)
            df_category = dataframes.df_revenue_category(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)
            df_partner1 = dataframes.df_revenue_partner1(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)
            df_partner2 = dataframes.df_revenue_partner2(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)
            df_table = dataframes.df_table_revenue(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)


            fig = plots.revenue_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.revenue_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_cat_rev(df_category)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.pie_partner_rev(df_partner1)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            fig5 = plots.pie_partner_rev(df_partner2)
            graph5=json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('revenue.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
                    graph4=graph4, graph5=graph5, df=df_table)
           
        if company_name[0] == 'All' and studio_name[0] != 'All' and product_name[0] == 'All':

            df = dataframes.df_revenue_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)
            df_country = dataframes.df_revenue_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)
            df_category = dataframes.df_revenue_category(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)
            df_partner1 = dataframes.df_revenue_partner1(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)
            df_partner2 = dataframes.df_revenue_partner2(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)
            df_table = dataframes.df_table_revenue(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)


            fig = plots.revenue_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.revenue_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_cat_rev(df_category)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.pie_partner_rev(df_partner1)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            fig5 = plots.pie_partner_rev(df_partner2)
            graph5=json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('revenue.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
                    graph4=graph4, graph5=graph5, df=df_table)

        if company_name[0] == 'All' and studio_name[0] == 'All' and product_name[0] != 'All':

            df = dataframes.df_revenue_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)
            df_country = dataframes.df_revenue_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)
            df_category = dataframes.df_revenue_category(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)
            df_partner1 = dataframes.df_revenue_partner1(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)
            df_partner2 = dataframes.df_revenue_partner2(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)
            df_table = dataframes.df_table_revenue(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)


            fig = plots.revenue_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.revenue_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_cat_rev(df_category)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.pie_partner_rev(df_partner1)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            fig5 = plots.pie_partner_rev(df_partner2)
            graph5=json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('revenue.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
                    graph4=graph4, graph5=graph5, df=df_table)

        if company_name[0] != 'All' and studio_name[0] != 'All' and product_name[0] == 'All':

            df = dataframes.df_revenue_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)
            df_country = dataframes.df_revenue_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)
            df_category = dataframes.df_revenue_category(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)
            df_partner1 = dataframes.df_revenue_partner1(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)
            df_partner2 = dataframes.df_revenue_partner2(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)
            df_table = dataframes.df_table_revenue(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)


            fig = plots.revenue_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.revenue_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_cat_rev(df_category)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.pie_partner_rev(df_partner1)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            fig5 = plots.pie_partner_rev(df_partner2)
            graph5=json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('revenue.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
                    graph4=graph4, graph5=graph5, df=df_table)


        if company_name[0] != 'All' and studio_name[0] == 'All' and product_name[0] != 'All':


            df = dataframes.df_revenue_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)
            df_country = dataframes.df_revenue_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)
            df_category = dataframes.df_revenue_category(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)
            df_partner1 = dataframes.df_revenue_partner1(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)
            df_partner2 = dataframes.df_revenue_partner2(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)
            df_table = dataframes.df_table_revenue(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)


            fig = plots.revenue_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.revenue_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_cat_rev(df_category)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.pie_partner_rev(df_partner1)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            fig5 = plots.pie_partner_rev(df_partner2)
            graph5=json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('revenue.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
                    graph4=graph4, graph5=graph5, df=df_table)


        if company_name[0] == 'All' and studio_name[0] != 'All' and product_name[0] != 'All':


            df = dataframes.df_revenue_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)
            df_country = dataframes.df_revenue_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)
            df_category = dataframes.df_revenue_category(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)
            df_partner1 = dataframes.df_revenue_partner1(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)
            df_partner2 = dataframes.df_revenue_partner2(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)
            df_table = dataframes.df_table_revenue(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)


            fig = plots.revenue_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.revenue_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_cat_rev(df_category)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.pie_partner_rev(df_partner1)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            fig5 = plots.pie_partner_rev(df_partner2)
            graph5=json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('revenue.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
                    graph4=graph4, graph5=graph5, df=df_table)

        if company_name[0] != 'All' and studio_name[0] != 'All' and product_name[0] != 'All':

            df = dataframes.df_revenue_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)
            df_country = dataframes.df_revenue_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)
            df_category = dataframes.df_revenue_category(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)
            df_partner1 = dataframes.df_revenue_partner1(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)
            df_partner2 = dataframes.df_revenue_partner2(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)
            df_table = dataframes.df_table_revenue(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)


            fig = plots.revenue_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.revenue_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_cat_rev(df_category)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.pie_partner_rev(df_partner1)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            fig5 = plots.pie_partner_rev(df_partner2)
            graph5=json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('revenue.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
                    graph4=graph4, graph5=graph5, df=df_table)


    df = dataframes.df_revenue_month_nf()
    df_country = dataframes.df_revenue_country_nf()
    df_category = dataframes.df_revenue_category_nf()
    df_partner1 = dataframes.df_revenue_partner1_nf()
    df_partner2 = dataframes.df_revenue_partner2_nf()
    df_table = dataframes.df_table_revenue_nf()


    fig = plots.revenue_by_month_plot(df)
    graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig2 = plots.revenue_by_country_plot(df_country)
    graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    fig3 = plots.pie_cat_rev(df_category)
    graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    fig4 = plots.pie_partner_rev(df_partner1)
    graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    fig5 = plots.pie_partner_rev(df_partner2)
    graph5=json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('revenue.html', form=form, graph=graph, graph2=graph2, graph3=graph3, 
            graph4=graph4, graph5=graph5, df=df_table)







#################################### Marketing Page ########################################



@app.route('/marketing/', methods=['GET',"POST"])
def marketing():
    form = FilterForm()
    form.company_name.choices=['All'] + utils.unique_value('Company')
    form.studio_name.choices=['All']+ utils.unique_value('Studio')
    form.product_name.choices=['All']+ utils.unique_value('Project')
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        company_name = form.company_name.data
        studio_name = form.studio_name.data
        product_name = form.product_name.data
        if company_name[0] == 'All' and studio_name[0] == 'All' and product_name[0] == 'All':

            df = dataframes.df_marketing_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")
            df_country = dataframes.df_marketing_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")
            df_partner = dataframes.df_marketing_partner(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")
            df_table = dataframes.df_table_marketing(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")


            fig = plots.marketing_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.marketing_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_partner_marketing(df_partner)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('marketing.html', form=form, graph=graph, graph2=graph2, graph3=graph3, df=df_table)

        if company_name[0] != 'All' and studio_name[0] == 'All' and product_name[0] == 'All':


            df = dataframes.df_marketing_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)
            df_country = dataframes.df_marketing_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)
            df_partner = dataframes.df_marketing_partner(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)
            df_table = dataframes.df_table_marketing(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)


            fig = plots.marketing_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.marketing_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_partner_marketing(df_partner)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('marketing.html', form=form, graph=graph, graph2=graph2, graph3=graph3, df=df_table)
           
        if company_name[0] == 'All' and studio_name[0] != 'All' and product_name[0] == 'All':

            df = dataframes.df_marketing_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)
            df_country = dataframes.df_marketing_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)
            df_partner = dataframes.df_marketing_partner(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)
            df_table = dataframes.df_table_marketing(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)


            fig = plots.marketing_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.marketing_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_partner_marketing(df_partner)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('marketing.html', form=form, graph=graph, graph2=graph2, graph3=graph3, df=df_table)


        if company_name[0] == 'All' and studio_name[0] == 'All' and product_name[0] != 'All':

            df = dataframes.df_marketing_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)
            df_country = dataframes.df_marketing_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)
            df_partner = dataframes.df_marketing_partner(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)
            df_table = dataframes.df_table_marketing(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)


            fig = plots.marketing_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.marketing_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_partner_marketing(df_partner)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('marketing.html', form=form, graph=graph, graph2=graph2, graph3=graph3, df=df_table)

        if company_name[0] != 'All' and studio_name[0] != 'All' and product_name[0] == 'All':

            df = dataframes.df_marketing_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)
            df_country = dataframes.df_marketing_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)
            df_partner = dataframes.df_marketing_partner(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)
            df_table = dataframes.df_table_marketing(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)


            fig = plots.marketing_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.marketing_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_partner_marketing(df_partner)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('marketing.html', form=form, graph=graph, graph2=graph2, graph3=graph3, df=df_table)


        if company_name[0] != 'All' and studio_name[0] == 'All' and product_name[0] != 'All':


            df = dataframes.df_marketing_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)
            df_country = dataframes.df_marketing_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)
            df_partner = dataframes.df_marketing_partner(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)
            df_table = dataframes.df_table_marketing(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)


            fig = plots.marketing_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.marketing_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_partner_marketing(df_partner)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('marketing.html', form=form, graph=graph, graph2=graph2, graph3=graph3, df=df_table)


        if company_name[0] == 'All' and studio_name[0] != 'All' and product_name[0] != 'All':


            df = dataframes.df_marketing_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)
            df_country = dataframes.df_marketing_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)
            df_partner = dataframes.df_marketing_partner(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)
            df_table = dataframes.df_table_marketing(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)


            fig = plots.marketing_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.marketing_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_partner_marketing(df_partner)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('marketing.html', form=form, graph=graph, graph2=graph2, graph3=graph3, df=df_table)

        if company_name[0] != 'All' and studio_name[0] != 'All' and product_name[0] != 'All':

            df = dataframes.df_marketing_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)
            df_country = dataframes.df_marketing_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)
            df_partner = dataframes.df_marketing_partner(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)
            df_table = dataframes.df_table_marketing(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)


            fig = plots.marketing_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.marketing_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_partner_marketing(df_partner)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('marketing.html', form=form, graph=graph, graph2=graph2, graph3=graph3, df=df_table)


    df = dataframes.df_marketing_month_nf()
    df_country = dataframes.df_marketing_country_nf()
    df_partner = dataframes.df_marketing_partner_nf()
    df_table = dataframes.df_table_marketing_nf()


    fig = plots.marketing_by_month_plot(df)
    graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig2 = plots.marketing_by_country_plot(df_country)
    graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    fig3 = plots.pie_partner_marketing(df_partner)
    graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('marketing.html', form=form, graph=graph, graph2=graph2, graph3=graph3, df=df_table)






@app.route('/development/', methods=['GET',"POST"])
def development():
    form = FilterForm()
    form.company_name.choices=['All'] + utils.unique_value('Company')
    form.studio_name.choices=['All']+ utils.unique_value('Studio')
    form.product_name.choices=['All']+ utils.unique_value('Project')
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        company_name = form.company_name.data
        studio_name = form.studio_name.data
        product_name = form.product_name.data
        if company_name[0] == 'All' and studio_name[0] == 'All' and product_name[0] == 'All':

            df = dataframes.df_dev_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")
            df_country = dataframes.df_dev_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")
            df_category = dataframes.df_dev_category(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")
            df_partner = dataframes.df_dev_partner(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")
            df_table = dataframes.df_table_dev(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'")


            fig = plots.dev_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.dev_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_cat_dev(df_category)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.pie_partner_dev(df_partner)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('development.html', form=form, graph=graph, graph2=graph2, graph3=graph3, graph4=graph4, df=df_table)

        if company_name[0] != 'All' and studio_name[0] == 'All' and product_name[0] == 'All':


            df = dataframes.df_dev_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)
            df_country = dataframes.df_dev_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)
            df_category = dataframes.df_dev_category(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)
            df_partner = dataframes.df_dev_partner(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)
            df_table = dataframes.df_table_dev(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name)


            fig = plots.dev_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.dev_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_cat_dev(df_category)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.pie_partner_dev(df_partner)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('development.html', form=form, graph=graph, graph2=graph2, graph3=graph3, graph4=graph4, df=df_table)
           
        if company_name[0] == 'All' and studio_name[0] != 'All' and product_name[0] == 'All':

            df = dataframes.df_dev_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)
            df_country = dataframes.df_dev_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)
            df_category = dataframes.df_dev_category(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)
            df_partner = dataframes.df_dev_partner(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)
            df_table = dataframes.df_table_dev(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name)


            fig = plots.dev_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.dev_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_cat_dev(df_category)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.pie_partner_dev(df_partner)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('development.html', form=form, graph=graph, graph2=graph2, graph3=graph3, graph4=graph4, df=df_table)


        if company_name[0] == 'All' and studio_name[0] == 'All' and product_name[0] != 'All':

            df = dataframes.df_dev_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)
            df_country = dataframes.df_dev_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)
            df_category = dataframes.df_dev_category(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)
            df_partner = dataframes.df_dev_partner(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)
            df_table = dataframes.df_table_dev(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", product_name=product_name)


            fig = plots.dev_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.dev_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_cat_dev(df_category)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.pie_partner_dev(df_partner)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('development.html', form=form, graph=graph, graph2=graph2, graph3=graph3, graph4=graph4, df=df_table)

        if company_name[0] != 'All' and studio_name[0] != 'All' and product_name[0] == 'All':

            df = dataframes.df_dev_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)
            df_country = dataframes.df_dev_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)
            df_category = dataframes.df_dev_category(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)
            df_partner = dataframes.df_dev_partner(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)
            df_table = dataframes.df_table_dev(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name)


            fig = plots.dev_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.dev_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_cat_dev(df_category)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.pie_partner_dev(df_partner)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('development.html', form=form, graph=graph, graph2=graph2, graph3=graph3, graph4=graph4, df=df_table)


        if company_name[0] != 'All' and studio_name[0] == 'All' and product_name[0] != 'All':


            df = dataframes.df_dev_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)
            df_country = dataframes.df_dev_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)
            df_category = dataframes.df_dev_category(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)
            df_partner = dataframes.df_dev_partner(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)
            df_table = dataframes.df_table_dev(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, product_name=product_name)


            fig = plots.dev_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.dev_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_cat_dev(df_category)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.pie_partner_dev(df_partner)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('development.html', form=form, graph=graph, graph2=graph2, graph3=graph3, graph4=graph4, df=df_table)


        if company_name[0] == 'All' and studio_name[0] != 'All' and product_name[0] != 'All':

            df = dataframes.df_dev_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)
            df_country = dataframes.df_dev_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)
            df_category = dataframes.df_dev_category(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)
            df_partner = dataframes.df_dev_partner(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)
            df_table = dataframes.df_table_dev(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", studio_name=studio_name, product_name=product_name)


            fig = plots.dev_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.dev_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_cat_dev(df_category)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.pie_partner_dev(df_partner)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('development.html', form=form, graph=graph, graph2=graph2, graph3=graph3, graph4=graph4, df=df_table)


        if company_name[0] != 'All' and studio_name[0] != 'All' and product_name[0] != 'All':

            df = dataframes.df_dev_month(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)
            df_country = dataframes.df_dev_country(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)
            df_category = dataframes.df_dev_category(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)
            df_partner = dataframes.df_dev_partner(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)
            df_table = dataframes.df_table_dev(start_date="'"+str(start_date)+"'", end_date="'"+str(end_date)+"'", company_name=company_name, studio_name=studio_name, product_name=product_name)


            fig = plots.dev_by_month_plot(df)
            graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            fig2 = plots.dev_by_country_plot(df_country)
            graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            fig3 = plots.pie_cat_dev(df_category)
            graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            fig4 = plots.pie_partner_dev(df_partner)
            graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('development.html', form=form, graph=graph, graph2=graph2, graph3=graph3, graph4=graph4, df=df_table)

    df = dataframes.df_dev_month_nf()
    df_country = dataframes.df_dev_country_nf()
    df_category = dataframes.df_dev_category_nf()
    df_partner = dataframes.df_dev_partner_nf()
    df_table = dataframes.df_table_dev_nf()


    fig = plots.dev_by_month_plot(df)
    graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig2 = plots.dev_by_country_plot(df_country)
    graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    fig3 = plots.pie_cat_dev(df_category)
    graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    fig4 = plots.pie_partner_dev(df_partner)
    graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('development.html', form=form, graph=graph, graph2=graph2, graph3=graph3, graph4=graph4, df=df_table)









@app.route('/test/')
def test():
    df = dataframes.df_main_nf()
    return render_template('test.html', df=df)















class PredictionsForm(FlaskForm):
    product_name = SelectField('Product Name', choices = [], 
        validators=[DataRequired()], validate_choice=True)
    window_size = IntegerField('Window Size', 
        validators=[DataRequired()])
    epoch = IntegerField('Epoch', validators=[DataRequired()])
    months_pred = IntegerField('No of months to predict', validators=[DataRequired()])
    train_test = DecimalField('Train Set portion', validators=[DataRequired()])
    submit = SubmitField('Make Predictions')
    submit = SubmitField('Save forecast')


@app.route('/predictions/', methods=['GET',"POST"])
def predictions():
    form = PredictionsForm()
    form.product_name.choices=utils.unique_value('Project')
    
    if form.validate_on_submit():
        product_name = form.product_name.data
        window_size = form.window_size.data
        epoch = form.epoch.data
        months_pred = form.months_pred.data
        train_test = form.train_test.data
        df = dataframes.df_model()
        test_preds, loss_per_epoch, score, df_original, df_normalized = preds.model_creation(df=df, 
            train_portion=train_test, window_size=window_size, 
            epochs=epoch, product=product_name)
        act_preds = preds.forecast(df=df, nr_months=months_pred, window_size=window_size, 
            epochs=epoch, product=product_name)
        fig = plots.original_plot(df_original)
        graph=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        fig2 = plots.normalized_plot(df_normalized)
        graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
        fig3 = plots.loss_per_epoch_plot(loss_per_epoch)
        graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
        fig4 = plots.test_pred(test_preds)
        graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
        fig5 = plots.forecast_plot(act_preds)
        graph5=json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
        if request.form['submit'] == 'Make Predictions':
            return render_template('predictions.html', form=form, 
                graph=graph, graph2=graph2, graph3=graph3, 
                graph4=graph4, graph5=graph5, score=score)
        if request.form['submit'] == 'Save forecast':
            utils.save_to_s3(act_preds, product_name)
            flash('File was successfully saved to S3')
            return render_template('predictions_no_graph.html', form=form)
        
    return render_template('predictions_no_graph.html', form=form)









### TODO
# https://www.youtube.com/watch?v=I2dJuNwlIH0
# Dynamic Select Fields
@app.route('/studio/<company>')
def studio(company):
    df = utils.read_file_s3(utils.bucket)
    studios = list(df[df['Company'].isin([company])]['Studio'].unique())
    studioObj = {}
    studios_list = list()
    for studio in studios:
        studios_list.append(studio)
        
    studioObj['name'] = studios_list
    return jsonify( {'studios': studioObj})



