import utils
import pandas as pd
import numpy as np



##############Profit Page#######################

df_all = utils.read_file_s3(utils.bucket)
df_all['Date'] = pd.to_datetime(df_all['Date'])
df_predictions = utils.read_file_s3(utils.bucket2)

#############Main Dataframe#####################

###No Filters
def df_main_nf():
	df = df_all.groupby('Date').sum()['Amount_USD'].reset_index()
	df['color'] = np.where(df['Amount_USD']<0, '#F43B76', '#36CE53')
	df['RT'] = df['Amount_USD'].cumsum()
	df['color_RT'] = np.where(df['RT']<0, '#F43B76', '#36CE53')

	return df

def df_project_nf():
	df_project = df_all.groupby('Project').sum()['Amount_USD'].reset_index()
	df_project['color'] = np.where(df_project['Amount_USD']<0, '#F43B76', '#36CE53')
	return df_project

def df_table_nf():
	df_table = df_all.groupby(['Date', 'Project']).sum()['Amount_USD'].reset_index()
	return df_table



def df_main(start_date, end_date, company_name=utils.unique_value('Company'),\
 studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):

	df_filtered = df_all[(df_all['Date']>=start_date)&(df_all['Date']<=end_date)\
	&(df_all['Company'].isin(company_name))&(df_all['Studio'].isin(studio_name))\
	&(df_all['Project'].isin(product_name))]
	df = df_filtered.groupby('Date').sum()['Amount_USD'].reset_index()
	df['color'] = np.where(df['Amount_USD']<0, '#F43B76', '#36CE53')
	df['RT'] = df['Amount_USD'].cumsum()
	df['color_RT'] = np.where(df['RT']<0, '#F43B76', '#36CE53')

	return df

def df_project(start_date, end_date, company_name=utils.unique_value('Company'),\
 studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):

	df_filtered = df_all[(df_all['Date']>=start_date)&(df_all['Date']<=end_date)\
	&(df_all['Company'].isin(company_name))&(df_all['Studio'].isin(studio_name))\
	&(df_all['Project'].isin(product_name))]
	df_project = df_filtered.groupby('Project').sum()['Amount_USD'].reset_index()
	df_project['color'] = np.where(df_project['Amount_USD']<0, '#F43B76', '#36CE53')
	return df_project

def df_preds(company_name=utils.unique_value('Company'),\
 studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):

	df_filtered = df_predictions[(df_predictions['Company'].isin(company_name))&(df_predictions['Studio'].isin(studio_name))\
	&(df_predictions['Project'].isin(product_name))]
	preds = df_filtered.groupby('Date').sum()['Amount_USD'].reset_index()
	return preds


def df_table(start_date, end_date, company_name=utils.unique_value('Company'),\
 studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):

	df_filtered = df_all[(df_all['Date']>=start_date)&(df_all['Date']<=end_date)\
	&(df_all['Company'].isin(company_name))&(df_all['Studio'].isin(studio_name))\
	&(df_all['Project'].isin(product_name))]
	df_table = df_filtered.groupby(['Date', 'Project']).sum()['Amount_USD'].reset_index()
	return df_table
