import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import os
import mysql.connector
import MySQLdb
load_dotenv()


mydb = MySQLdb.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True,
    ssl_mode="VERIFY_IDENTITY",
    ssl={
        "ca": "C:\ssl\certs\cacert.pem"
    }
)

cursor = mydb.cursor()