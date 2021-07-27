import pandas as pd
from configparser import ConfigParser
import os
import logging

from airflow.providers.amazon.aws.hooks.s3 import S3Hook


def upload_to_s3(year, week):
    """
    upload the created csv files into S3 bucket

    file name formats should be:
    YYYY_WW_menu.csv
    YYYY_WW_TOP_10.csv
    """
    # read the config file
    cp = ConfigParser()
    cp.read("config.ini")

    # read connection params from config file
    s3_conn_id = cp["s3_conn"]["conn_id"]
    bucket_name = cp["s3_conn"]["bucket_name"]

    # files to be uploaded
    fname_recipes = str(year) + "_" + str(week) + "_menu.csv"
    fname_top_recipes = str(year) + "_" + str(week) + "_TOP_10.csv"

    if not (os.path.exists(fname_recipes) and os.path.exists(fname_top_recipes)):
        logging.error("Unable to upload to S3. CSV files do not exists.")
        return

    # connect to s3
    s3_hook = S3Hook(aws_conn_id=s3_conn_id)

    try:
        # load csv files to s3
        s3_hook.load_file(fname_recipes, key=fname_recipes, bucket_name=bucket_name, replace=True)
        s3_hook.load_file(fname_top_recipes, key=fname_top_recipes, bucket_name=bucket_name, replace=True)
    except Exception as e:
        logging.error("S3 connection Error:%s",e)
    else:
        logging.info("recipes uploaded to S3:%s.", bucket_name)
        
        # remove local csv copies
 #       os.remove(fname_recipes)
 #       os.remove(fname_top_recipes)
