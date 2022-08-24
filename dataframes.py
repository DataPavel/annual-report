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
	df['color'] = np.where(df['Amount_USD']<0, '#F43B76', '#037A9C')
	df['RT'] = df['Amount_USD'].cumsum()
	df['color_RT'] = np.where(df['RT']<0, '#F43B76', '#36CE53')

	return df

def df_project_nf():
	df_project = df_all.groupby('Project').sum()['Amount_USD'].reset_index()
	df_project['color'] = np.where(df_project['Amount_USD']<0, '#F43B76', '#037A9C')
	return df_project

def df_table_nf():
	df_table = df_all.groupby(['Project']).sum()['Amount_USD'].reset_index().sort_values(by=['Project'])
	return df_table

def df_preds_nf():

	preds = df_predictions.groupby(['Date', 'Date_str']).sum()['Amount_USD'].reset_index()
	preds['color'] = np.where(preds['Amount_USD']<0, '#F43B76', '#36CE53')
	return preds






### With filters

def df_main(start_date, end_date, company_name=utils.unique_value('Company'),\
 studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):

	df_filtered = df_all[(df_all['Date']>=start_date)&(df_all['Date']<=end_date)\
	&(df_all['Company'].isin(company_name))&(df_all['Studio'].isin(studio_name))\
	&(df_all['Project'].isin(product_name))]
	df = df_filtered.groupby(['Date', 'Date_str']).sum()['Amount_USD'].reset_index()
	df['color'] = np.where(df['Amount_USD']<0, '#F43B76', '#037A9C')
	df['RT'] = df['Amount_USD'].cumsum()
	df['color_RT'] = np.where(df['RT']<0, '#F43B76', '#36CE53')

	return df

def df_project(start_date, end_date, company_name=utils.unique_value('Company'),\
 studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):

	df_filtered = df_all[(df_all['Date']>=start_date)&(df_all['Date']<=end_date)\
	&(df_all['Company'].isin(company_name))&(df_all['Studio'].isin(studio_name))\
	&(df_all['Project'].isin(product_name))]
	df_project = df_filtered.groupby('Project').sum()['Amount_USD'].reset_index()
	df_project['color'] = np.where(df_project['Amount_USD']<0, '#F43B76', '#037A9C')
	return df_project

def df_preds(start_date, company_name=utils.unique_value('Company'),\
 studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):

	df_filtered = df_predictions[(df_predictions['Date']>=start_date)&(df_predictions['Company'].isin(company_name))&(df_predictions['Studio'].isin(studio_name))\
	&(df_predictions['Project'].isin(product_name))]
	preds = df_filtered.groupby(['Date', 'Date_str']).sum()['Amount_USD'].reset_index()
	preds['color'] = np.where(preds['Amount_USD']<0, '#F43B76', '#36CE53')
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
df_all_revenue = df_all_revenue[df_all_revenue['Category1']=='Revenue']
df_all_revenue['Date'] = pd.to_datetime(df_all_revenue['Date'])
df_all_revenue['Date_str'] = df_all_revenue['Date'].apply(lambda x: x.strftime("%Y-%m"))

###No Filters
def df_revenue_month_nf():
	df = df_all_revenue.groupby(['Date', 'Date_str', 'Category2']).sum()['Amount_USD'].reset_index()
	return df

def df_revenue_country_nf():
	df_country = df_all_revenue.groupby('Country').sum()['Amount_USD'].reset_index().sort_values('Amount_USD')
	return df_country

def df_revenue_category_nf():
	df_category = df_all_revenue.groupby('Category2').sum()['Amount_USD'].reset_index()
	return df_category

def df_revenue_partner1_nf():
	df_partner1 = df_all_revenue[df_all_revenue['Category2']=='Mobile IAP']\
	.groupby('Counterparty').sum()['Amount_USD'].reset_index()
	return df_partner1

def df_revenue_partner2_nf():
	df_partner2 = df_all_revenue[df_all_revenue['Category2']=='Revenue from Ads']\
	.groupby('Counterparty').sum()['Amount_USD'].reset_index()
	return df_partner2

def df_table_revenue_nf():
	df_table = df_all_revenue.groupby(['Category2']).sum()['Amount_USD'].reset_index().sort_values(by=['Category2'])
	return df_table


###With filters

def df_revenue_month(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):
	df_filtered = df_all_revenue[(df_all_revenue['Date']>=start_date)&(df_all_revenue['Date']<=end_date)\
	&(df_all_revenue['Company'].isin(company_name))&(df_all_revenue['Studio'].isin(studio_name))\
	&(df_all_revenue['Project'].isin(product_name))]

	df = df_filtered.groupby(['Date', 'Date_str', 'Category2']).sum()['Amount_USD'].reset_index()
	return df

def df_revenue_country(start_date, end_date, company_name=utils.unique_value('Company'),\
	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):
	df_filtered = df_all_revenue[(df_all_revenue['Date']>=start_date)&(df_all_revenue['Date']<=end_date)\
	&(df_all_revenue['Company'].isin(company_name))&(df_all_revenue['Studio'].isin(studio_name))\
	&(df_all_revenue['Project'].isin(product_name))]
	df_country = df_filtered.groupby('Country').sum()['Amount_USD'].reset_index().sort_values(by=['Amount_USD'])
	return df_country

def df_revenue_category(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):

	df_filtered = df_all_revenue[(df_all_revenue['Date']>=start_date)&(df_all_revenue['Date']<=end_date)\
	&(df_all_revenue['Company'].isin(company_name))&(df_all_revenue['Studio'].isin(studio_name))\
	&(df_all_revenue['Project'].isin(product_name))]

	df_category = df_filtered.groupby('Category2').sum()['Amount_USD'].reset_index()
	return df_category

def df_revenue_partner1(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):

	df_filtered = df_all_revenue[(df_all_revenue['Date']>=start_date)&(df_all_revenue['Date']<=end_date)\
	&(df_all_revenue['Company'].isin(company_name))&(df_all_revenue['Studio'].isin(studio_name))\
	&(df_all_revenue['Project'].isin(product_name))]

	df_partner1 = df_filtered[df_filtered['Category2']=='Mobile IAP']\
	.groupby('Counterparty').sum()['Amount_USD'].reset_index()
	return df_partner1

def df_revenue_partner2(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):
	
	df_filtered = df_all_revenue[(df_all_revenue['Date']>=start_date)&(df_all_revenue['Date']<=end_date)\
	&(df_all_revenue['Company'].isin(company_name))&(df_all_revenue['Studio'].isin(studio_name))\
	&(df_all_revenue['Project'].isin(product_name))]

	df_partner2 = df_filtered[df_filtered['Category2']=='Revenue from Ads']\
	.groupby('Counterparty').sum()['Amount_USD'].reset_index()
	return df_partner2

def df_table_revenue(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):
	
	df_filtered = df_all_revenue[(df_all_revenue['Date']>=start_date)&(df_all_revenue['Date']<=end_date)\
	&(df_all_revenue['Company'].isin(company_name))&(df_all_revenue['Studio'].isin(studio_name))\
	&(df_all_revenue['Project'].isin(product_name))]

	df_table = df_filtered.groupby(['Category2']).sum()['Amount_USD'].reset_index().sort_values(by=['Category2'])
	return df_table







############## Marketing Page #######################

df_all_marketing = utils.read_file_s3(utils.bucket)
df_all_marketing = df_all_marketing[df_all_marketing['Category1']=='Marketing']
df_all_marketing['Date'] = pd.to_datetime(df_all_marketing['Date'])
df_all_marketing['Date_str'] = df_all_marketing['Date'].apply(lambda x: x.strftime("%Y-%m"))
df_all_marketing['amount_abs'] = df_all_marketing['Amount_USD'].apply(lambda x: x*-1)

###No Filters
def df_marketing_month_nf():
	df = df_all_marketing.groupby(['Date', 'Date_str', 'Category2']).sum()['amount_abs'].reset_index()
	return df

def df_marketing_country_nf():
	df_country = df_all_marketing.groupby('Country').sum()['amount_abs'].reset_index().sort_values('amount_abs')
	return df_country

def df_marketing_partner_nf():
	df_partner = df_all_marketing.groupby('Counterparty').sum()['amount_abs'].reset_index()
	return df_partner

def df_table_marketing_nf():
	df_table = df_all_marketing.groupby(['Counterparty']).sum()['amount_abs'].reset_index().sort_values(by=['amount_abs'])
	return df_table


###With filters

def df_marketing_month(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):
	df_filtered = df_all_marketing[(df_all_marketing['Date']>=start_date)&(df_all_marketing['Date']<=end_date)\
	&(df_all_marketing['Company'].isin(company_name))&(df_all_marketing['Studio'].isin(studio_name))\
	&(df_all_marketing['Project'].isin(product_name))]

	df = df_filtered.groupby(['Date', 'Date_str', 'Category2']).sum()['amount_abs'].reset_index()
	return df

def df_marketing_country(start_date, end_date, company_name=utils.unique_value('Company'),\
	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):
	df_filtered = df_all_marketing[(df_all_marketing['Date']>=start_date)&(df_all_marketing['Date']<=end_date)\
	&(df_all_marketing['Company'].isin(company_name))&(df_all_marketing['Studio'].isin(studio_name))\
	&(df_all_marketing['Project'].isin(product_name))]
	df_country = df_filtered.groupby('Country').sum()['amount_abs'].reset_index().sort_values(by=['amount_abs'])
	return df_country

def df_marketing_partner(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):

	df_filtered = df_all_marketing[(df_all_marketing['Date']>=start_date)&(df_all_marketing['Date']<=end_date)\
	&(df_all_marketing['Company'].isin(company_name))&(df_all_marketing['Studio'].isin(studio_name))\
	&(df_all_marketing['Project'].isin(product_name))]

	df_partner = df_filtered.groupby('Counterparty').sum()['amount_abs'].reset_index()
	return df_partner

def df_table_marketing(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):
	
	df_filtered = df_all_marketing[(df_all_marketing['Date']>=start_date)&(df_all_marketing['Date']<=end_date)\
	&(df_all_marketing['Company'].isin(company_name))&(df_all_marketing['Studio'].isin(studio_name))\
	&(df_all_marketing['Project'].isin(product_name))]

	df_table = df_filtered.groupby(['Counterparty']).sum()['amount_abs'].reset_index().sort_values(by=['amount_abs'], ascending=False)
	return df_table





############## Development Page #######################

df_all_dev = utils.read_file_s3(utils.bucket)
df_all_dev = df_all_dev[df_all_dev['Category1']=='Development']
df_all_dev['Date'] = pd.to_datetime(df_all_dev['Date'])
df_all_dev['Date_str'] = df_all_dev['Date'].apply(lambda x: x.strftime("%Y-%m"))
df_all_dev['amount_abs'] = df_all_dev['Amount_USD'].apply(lambda x: x*-1)

###No Filters
def df_dev_month_nf():
	df = df_all_dev.groupby(['Date', 'Date_str', 'Category2']).sum()['amount_abs'].reset_index()
	return df

def df_dev_country_nf():
	df_country = df_all_dev.groupby('Country').sum()['amount_abs'].reset_index().sort_values('amount_abs')
	return df_country

def df_dev_category_nf():
	df_category = df_all_dev.groupby('Category2').sum()['amount_abs'].reset_index()
	return df_category

def df_dev_partner_nf():
	df_partner = df_all_dev.groupby('Counterparty').sum()['amount_abs'].reset_index()
	return df_partner

def df_table_dev_nf():
	df_table = df_all_dev.groupby(['Counterparty']).sum()['amount_abs'].reset_index().sort_values(by=['amount_abs'])
	return df_table


###With filters

def df_dev_month(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):
	df_filtered = df_all_dev[(df_all_dev['Date']>=start_date)&(df_all_dev['Date']<=end_date)\
	&(df_all_dev['Company'].isin(company_name))&(df_all_dev['Studio'].isin(studio_name))\
	&(df_all_dev['Project'].isin(product_name))]

	df = df_filtered.groupby(['Date', 'Date_str', 'Category2']).sum()['amount_abs'].reset_index()
	return df

def df_dev_country(start_date, end_date, company_name=utils.unique_value('Company'),\
	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):
	df_filtered = df_all_dev[(df_all_dev['Date']>=start_date)&(df_all_dev['Date']<=end_date)\
	&(df_all_dev['Company'].isin(company_name))&(df_all_dev['Studio'].isin(studio_name))\
	&(df_all_dev['Project'].isin(product_name))]
	df_country = df_filtered.groupby('Country').sum()['amount_abs'].reset_index().sort_values(by=['amount_abs'])
	return df_country

def df_dev_category(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):

	df_filtered = df_all_dev[(df_all_dev['Date']>=start_date)&(df_all_dev['Date']<=end_date)\
	&(df_all_dev['Company'].isin(company_name))&(df_all_dev['Studio'].isin(studio_name))\
	&(df_all_dev['Project'].isin(product_name))]

	df_category = df_filtered.groupby('Category2').sum()['amount_abs'].reset_index()
	return df_category

def df_dev_partner(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):

	df_filtered = df_all_dev[(df_all_dev['Date']>=start_date)&(df_all_dev['Date']<=end_date)\
	&(df_all_dev['Company'].isin(company_name))&(df_all_dev['Studio'].isin(studio_name))\
	&(df_all_dev['Project'].isin(product_name))]

	df_partner = df_filtered.groupby('Counterparty').sum()['amount_abs'].reset_index()
	return df_partner

def df_table_dev(start_date, end_date, company_name=utils.unique_value('Company'),\
 	studio_name=utils.unique_value('Studio'), product_name=utils.unique_value('Project')):
	
	df_filtered = df_all_dev[(df_all_dev['Date']>=start_date)&(df_all_dev['Date']<=end_date)\
	&(df_all_dev['Company'].isin(company_name))&(df_all_dev['Studio'].isin(studio_name))\
	&(df_all_dev['Project'].isin(product_name))]

	df_table = df_filtered.groupby(['Counterparty']).sum()['amount_abs'].reset_index().sort_values(by=['amount_abs'], ascending=False)
	return df_table



#####################Predictions Page###########################

def df_model():
	df = df_all.groupby(['Date', 'Date_str', 'Company', 'Studio','Project']).sum()['Amount_USD'].reset_index()
	df['color'] = np.where(df['Amount_USD']<0, '#F43B76', '#037A9C')
	return df
















