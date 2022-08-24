import boto3
from dotenv import load_dotenv
import os
from io import StringIO
import pandas as pd

# Config-----------------------------------------------------------------


def configure():
    load_dotenv()

configure()

extentions = ['csv', 'xlsx', 'xls']


client = boto3.client(
    's3',
    aws_access_key_id = os.getenv('aws_access_key_id'), 
    aws_secret_access_key = os.getenv('aws_secret_access_key'),
    region_name = os.getenv('region_name')
)
bucket = os.getenv('bucket')
bucket2 = os.getenv('bucket2')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extentions


columns = ['Date', 'Company', 'Studio', 'Project', 'Category1', 'Category2', 'Country',
       'Country_code', 'OS', 'Counterparty', 'Amount_USD']

def read_file_s3(bucket_name):
	keys_list = list()
	for i in client.list_objects(Bucket=bucket_name)['Contents']:
	    keys_list.append(i['Key'])
	# Create the S3 object
	obj_list = list()
	for key in keys_list:
	    obj = client.get_object(
	        Bucket = bucket_name,
	        Key = key)
	    obj_list.append(obj)
	# Read data from the S3 object
	data_list = list()
	for obj in obj_list:
	    data = pd.read_csv(obj['Body'])
	    data_list.append(data)

	df = pd.concat(data_list, axis=0)

	return df

def unique_value(column_name):
	df = read_file_s3(bucket)
	col_value_unique = list(df[column_name].unique())
	return col_value_unique

################# Save DataFrame to S3 ###################################

def save_to_s3(df, file_name):
	csv_buf = StringIO()
	df.to_csv(csv_buf, header=True, index=False)
	csv_buf.seek(0)
	client.put_object(Bucket=bucket2, Body=csv_buf.getvalue(), Key=file_name+'.csv')