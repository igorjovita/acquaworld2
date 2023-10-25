import streamlit as st
from dotenv import load_dotenv
import os
import MySQLdb

load_dotenv()
connection = MySQLdb.connect(
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

