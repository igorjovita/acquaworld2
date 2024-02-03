import mysql.connector
import os



mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True)

cursor = mydb.cursor(buffered=True)


def obter_comissao(pratica):
    if pratica == 'DIVEMASTER':
        return 200.00
    elif pratica == 'RESCUE':
        return 150.00
    elif pratica == 'REVIEW':
        return 120.00
    else:
        return 75.00



