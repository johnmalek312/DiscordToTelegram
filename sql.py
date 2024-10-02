import random
import traceback
import data
import mysql.connector
from mysql.connector import cursor_cext
from dotenv import load_dotenv
import os

load_dotenv()

class sqlData:
    connected: bool = False
    connection: mysql.connector.connection_cext.CMySQLConnection
    cursor: mysql.connector.cursor_cext.CMySQLCursor
    f = '%Y-%m-%d %H:%M:%S'


def connect():
    try:
        sqlData.connection = mysql.connector.connect(host=os.getenv("HOST"),
                                                     database=os.getenv("DATABASE"),
                                                     user=os.getenv("USER"),
                                                     password=os.getenv("PASSWORD"))
        print("We have connected to sql database")
        sqlData.connected = True
        refresh()
        return True
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))
        sqlData.connected = False
        return False


def reconnect():
    try:
        sqlData.connected = False
        if sqlData.connection.is_connected():
            sqlData.cursor.close()
            sqlData.connection.close()
        connect()
    except Exception as e:
        print(e)
        print(traceback.format_exc())


def addChannel(discordID: int, telegramID: int, header: str, whitelist: int = None) -> bool:
    try:
        uniq = generate_unique_id()
        if whitelist is None:
            mySql_insert_query = f"""INSERT INTO forwarder (id, discord, telegram, header, whitelist) 
                                   VALUES 
                                   ({uniq}, {discordID}, {telegramID}, "{header}", NULL)"""
        else:
            mySql_insert_query = f"""INSERT INTO forwarder (id, discord, telegram, header, whitelist) 
                                   VALUES 
                                   ({uniq}, {discordID}, {telegramID}, "{header}", {whitelist})"""
        print(mySql_insert_query)
        sqlData.cursor = sqlData.connection.cursor()
        sqlData.cursor.execute(mySql_insert_query)
        sqlData.connection.commit()
        print(sqlData.cursor.rowcount,
              "Record inserted successfully into results table")
        sqlData.cursor.close()
        return True
    except mysql.connector.Error as error:
        print(traceback.format_exc())
        print("Failed to insert record into results table {}".format(error))
        sqlData.connected = False
        if sqlData.connection.is_connected():
            sqlData.cursor.close()
            sqlData.connection.close()
            print("MySQL connection is closed")
        connect()
        return False
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return False
        print(traceback.format_exc())
        sqlData.connected = False
        if sqlData.connection.is_connected():
            sqlData.cursor.close()
            sqlData.connection.close()
            print("MySQL connection is closed")
        connect()


def removeChannel(uniq: int) -> bool:
    try:
        sql = f"DELETE FROM forwarder WHERE id = {uniq}"
        sqlData.cursor = sqlData.connection.cursor()
        sqlData.cursor.execute(sql)
        sqlData.connection.commit()
        sqlData.cursor.close()
        return True
    except mysql.connector.Error as error:
        print(traceback.format_exc())
        print("Failed to insert record into results table {}".format(error))
        sqlData.connected = False
        if sqlData.connection.is_connected():
            sqlData.cursor.close()
            sqlData.connection.close()
            print("MySQL connection is closed")
        connect()
        return False
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return False
        print(traceback.format_exc())
        sqlData.connected = False
        if sqlData.connection.is_connected():
            sqlData.cursor.close()
            sqlData.connection.close()
            print("MySQL connection is closed")
        connect()


def getAllForwards() -> list:
    try:
        sql = f"SELECT * FROM forwarder"
        sqlData.cursor = sqlData.connection.cursor()
        sqlData.cursor.execute(sql)
        myresult = sqlData.cursor.fetchall()
        data.forwards = myresult
        sqlData.connection.commit()
        return myresult
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return False
        print(traceback.format_exc())
        sqlData.connected = False
        if sqlData.connection.is_connected():
            sqlData.cursor.close()
            sqlData.connection.close()
            print("MySQL connection is closed")
        connect()


def generate_unique_id():
    # Generate a random integer
    unique_id = random.randint(1000, 9999)
    sqlData.cursor = sqlData.connection.cursor(())

    # Query the "forwarder" table to see if the generated ID is already in use
    sqlData.cursor.execute('SELECT * FROM forwarder WHERE id=%s', (unique_id,))
    result = sqlData.cursor.fetchone()

    # If the ID is already in use, generate a new one and try again
    if result:
        return generate_unique_id()
    else:
        return unique_id


def refresh():
    data.forwards = getAllForwards()
