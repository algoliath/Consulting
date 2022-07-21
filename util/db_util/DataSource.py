import mysql.connector as connector


def getConnection():
    connection = connector.connect(host='localhost',
                                   user='root',
                                   password='db_password',
                                   database='consulting')
    return connection

