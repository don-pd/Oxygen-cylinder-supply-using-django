import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'donpd'
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE elderco")

print("ALL done!")