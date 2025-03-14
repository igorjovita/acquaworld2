import os
import mysql.connector
import streamlit as st

class DataBaseMysql:
    def __init__(self, ):
        self.__connection = None
        self.__cursor = None

    def connect(self):
        mydb = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USERNAME"),
            passwd=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME"),
            autocommit=True,
            ssl_disabled=True)
        self.__connection = mydb
        self.__cursor = self.__connection.cursor(buffered=True)
        return self.__cursor

    def disconnect(self):
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None

    def execute_query(self, query, params=None):
        try:

            cursor = self.connect()
            cursor.execute(query, params)

            if query.strip().startswith('SELECT') or query.strip().startswith('WITH'):
                result = cursor.fetchall()
                return result

            elif query.strip().startswith('INSERT INTO'):
                id_lastrow = cursor.lastrowid

                return id_lastrow

            elif query.strip().startswith('DELETE'):
                st.success('Dados excluidos com Sucesso!')

            elif query.strip().startswith('UPDATE'):
                st.success('Dados alterados com Sucesso!')

        except mysql.connector.Error as e:
            st.error(f"Error executing query: {e}")
            raise
        finally:
            self.disconnect()
