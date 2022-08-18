import utils
import pandas as pd
import numpy as np
from datetime import datetime



##############Profit Page#######################

df_all = utils.read_file_s3(utils.bucket)
df_all['Date'] = pd.to_datetime(df_all['Date'])
df_all['Date_str'] = df_all['Date'].apply(lambda x: x.strftime("%Y-%m"))
df_predictions = utils.read_file_s3(utils.bucket2)
df_predictions['Date'] = pd.to_datetime(df_predictions['Date'])
df_predictions['Date_str'] = df_predictions['Date'].apply(lambda x: x.strftime("%Y-%m"))



###No Filters
def df_main_nf():
	df = df_all.groupby(['Date', 'Date_str']).sum()['Amount_USD'].reset_index()
	df['color'] = np.where(df['Amount_USD']<0, '#F43B76', '#36CE53')
	df['RT'] = df['Amount_USD'].cumsum()
	df['color_RT'] = np.where(df['RT']<0, '#F43B76', '#36CE53')

	return df

def df_project_nf():
	df_project = df_all.groupby('Project').sum()['Amount_USD'].reset_index()
	df_project['color'] = np.where(df_project['Amount_USD']<0, '#F43B76', '#36CE53')
	return df_project

def df_table_nf():
	df_table = df_all.groupby(['Project']).sum()['Amount_USD'].reset_index().sort_values(by=['Project'])
	return df_table

### With filters

def df_main(start_date, end_date, company_name=utils.unique_value('Company'),\
 studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):

	df_filtered = df_all[(df_all['Date']>=start_date)&(df_all['Date']<=end_date)\
	&(df_all['Company'].isin(company_name))&(df_all['Studio'].isin(studio_name))\
	&(df_all['Project'].isin(product_name))]
	df = df_filtered.groupby(['Date', 'Date_str']).sum()['Amount_USD'].reset_index()
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
	preds = df_filtered.groupby(['Date', 'Date_str']).sum()['Amount_USD'].reset_index()
	return preds


def df_table(start_date, end_date, company_name=utils.unique_value('Company'),\
 studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):

	df_filtered = df_all[(df_all['Date']>=start_date)&(df_all['Date']<=end_date)\
	&(df_all['Company'].isin(company_name))&(df_all['Studio'].isin(studio_name))\
	&(df_all['Project'].isin(product_name))]
	df_table = df_filtered.groupby(['Project']).sum()['Amount_USD'].reset_index().sort_values(by=['Project'])
	return df_table



##############Revenue Page#######################

df_all_revenue = utils.read_file_s3(utils.bucket)
df_all_revenue = df_all_revenue[df_all_revenue['Category'].isin(['Mobile IAP', 'Revenue from Ads'])]
df_all_revenue['Date'] = pd.to_datetime(df_all_revenue['Date'])
df_all_revenue['Date_str'] = df_all_revenue['Date'].apply(lambda x: x.strftime("%Y-%m"))

###No Filters
def df_revenue_month_nf():
	df = df_all_revenue.groupby(['Date', 'Date_str', 'Category']).sum()['Amount_USD'].reset_index()
	return df

def df_revenue_country_nf():
	df_country = df_all_revenue.groupby('Country').sum()['Amount_USD'].reset_index()
	return df_country

def df_revenue_category_nf():
	df_category = df_all_revenue.groupby('Category').sum()['Amount_USD'].reset_index()
	return df_category

def df_revenue_partner1_nf():
	df_partner1 = df_all_revenue[df_all_revenue['Category']=='Mobile IAP']\
	.groupby('Counterparty').sum()['Amount_USD'].reset_index()
	return df_partner1

def df_revenue_partner2_nf():
	df_partner2 = df_all_revenue[df_all_revenue['Category']=='Revenue from Ads']\
	.groupby('Counterparty').sum()['Amount_USD'].reset_index()
	return df_partner2

def df_table_revenue_nf():
	df_table = df_all_revenue.groupby(['Category']).sum()['Amount_USD'].reset_index().sort_values(by=['Category'])
	return df_table


###With filters

def df_revenue_month(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):
	df_filtered = df_all_revenue[(df_all_revenue['Date']>=start_date)&(df_all_revenue['Date']<=end_date)\
	&(df_all_revenue['Company'].isin(company_name))&(df_all_revenue['Studio'].isin(studio_name))\
	&(df_all_revenue['Project'].isin(product_name))]

	df = df_filtered.groupby(['Date', 'Date_str', 'Category']).sum()['Amount_USD'].reset_index()
	return df

def df_revenue_country(start_date, end_date, company_name=utils.unique_value('Company'),\
	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):
	df_filtered = df_all_revenue[(df_all_revenue['Date']>=start_date)&(df_all_revenue['Date']<=end_date)\
	&(df_all_revenue['Company'].isin(company_name))&(df_all_revenue['Studio'].isin(studio_name))\
	&(df_all_revenue['Project'].isin(product_name))]
	df_country = df_filtered.groupby('Country').sum()['Amount_USD'].reset_index()
	return df_country

def df_revenue_category(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):

	df_filtered = df_all_revenue[(df_all_revenue['Date']>=start_date)&(df_all_revenue['Date']<=end_date)\
	&(df_all_revenue['Company'].isin(company_name))&(df_all_revenue['Studio'].isin(studio_name))\
	&(df_all_revenue['Project'].isin(product_name))]

	df_category = df_filtered.groupby('Category').sum()['Amount_USD'].reset_index()
	return df_category

def df_revenue_partner1(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):

	df_filtered = df_all_revenue[(df_all_revenue['Date']>=start_date)&(df_all_revenue['Date']<=end_date)\
	&(df_all_revenue['Company'].isin(company_name))&(df_all_revenue['Studio'].isin(studio_name))\
	&(df_all_revenue['Project'].isin(product_name))]

	df_partner1 = df_filtered[df_filtered['Category']=='Mobile IAP']\
	.groupby('Counterparty').sum()['Amount_USD'].reset_index()
	return df_partner1

def df_revenue_partner2(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):
	
	df_filtered = df_all_revenue[(df_all_revenue['Date']>=start_date)&(df_all_revenue['Date']<=end_date)\
	&(df_all_revenue['Company'].isin(company_name))&(df_all_revenue['Studio'].isin(studio_name))\
	&(df_all_revenue['Project'].isin(product_name))]

	df_partner2 = df_filtered[df_filtered['Category']=='Revenue from Ads']\
	.groupby('Counterparty').sum()['Amount_USD'].reset_index()
	return df_partner2

def df_table_revenue(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):
	
	df_filtered = df_all_revenue[(df_all_revenue['Date']>=start_date)&(df_all_revenue['Date']<=end_date)\
	&(df_all_revenue['Company'].isin(company_name))&(df_all_revenue['Studio'].isin(studio_name))\
	&(df_all_revenue['Project'].isin(product_name))]

	df_table = df_filtered.groupby(['Category']).sum()['Amount_USD'].reset_index().sort_values(by=['Category'])
	return df_table
























