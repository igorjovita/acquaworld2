import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import os
import mysql.connector
import MySQLdb
load_dotenv()


mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True,
    ssl_verify_identity=True,
    ssl_ca="C:\Users\acqua\Downloads\cacert-2023-08-22.pem")

cursor = mydb.cursor()