import os
import sys
import psycopg2



INIT_STATEMENTS = [


    """CREATE TABLE IF NOT EXISTS USERS (
  ID int PRIMARY KEY,
  PASS TEXT not null,
  FULL_NAME varchar,
  SCREEN_NAME varchar,
  EMAIL varchar,
  CREATED_AT date,
  BIRTH_YEAR int,
  LOCATION_ID int);""",

"""CREATE TABLE IF NOT EXISTS Locations (
  ID int PRIMARY KEY,
  COUNTRY varchar,
  CITY varchar,
  DISTRICT varchar);""",

"""CREATE TABLE IF NOT EXISTS Reviews (
  USER_ID int,
  BOOK_ID int,
  RATING int,
  DATE_RATED date,
  PRIMARY KEY (USER_ID, BOOK_ID));""",

"""ALTER TABLE Users ADD FOREIGN KEY (LOCATION_ID) REFERENCES Locations (ID);""",

"""ALTER TABLE Reviews ADD FOREIGN KEY (USER_ID) REFERENCES Users (ID);""",



]



def db_initialize():
    connection = psycopg2.connect("user='postgres' host='localhost' password='45581222' port='5432'")
    
    connection.autocommit = True

    cursor = connection.cursor()

    cursor.execute("SELECT datname FROM pg_database;")

    list_database = cursor.fetchall()
    #print(list_database)
    db_name = 'lovenletter'
    if (db_name,) in list_database:
        #db exists
        #cursor = connection.cursor()
        flag = True
    else:
        #db doesnt exist
        sql = '''CREATE database LovenLetter; '''

        

        cursor.execute(sql)
        try:

            url = "dbname='lovenletter' user='postgres' host='localhost' password='45581222'"

            statement ="CREATE EXTENSION pgcrypto;"
            with psycopg2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute(statement)
            
        finally:
            cursor.close()
        flag = True

    connection.close()
    return(flag)

def init_tables():
    url = "dbname='lovenletter' user='postgres' host='localhost' password='45581222'"
    with psycopg2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()