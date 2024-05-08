# recordDAOframework.py
#
# This file implements the Data Access Object used by record_rest_srv.py
# for all operations. It implements the following:
# 1) Get all records
# 2) Get one record by ID
# 3) Create a record
# 4) Update a record
# 5) Delete a record
# 
# David O'Connell
#
#------------------------------------------------------------------------

import mysql.connector as mc
from mysql.connector import cursor
from mysql.connector.errors import Error
import sys

import mysqldbcfg as cfg

# Create the class
class RecordDAO:
    connection = ''
    cursor =     ''
    host =       ''
    user =       ''
    password =   ''
    database =   ''
    
#------------------------------------------------------------------------

    def __init__(self):
        self.host     = cfg.mysqldb['host']
        self.user     = cfg.mysqldb['user']
        self.password = cfg.mysqldb['password']
        self.database = cfg.mysqldb['database']

#------------------------------------------------------------------------

    def get_cursor(self): 
        self.connection = mc.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

#------------------------------------------------------------------------
# Check if the database from the configuration file exists

    def db_check(self):
        exists = False
        try:
            print("Looking for",cfg.mysqldb['database'])
            # this will not return a cursor if the database doesn't exist and an exception will be thrown
            cursor = self.get_cursor()
            if cursor:
                exists = True
        except Error as e:
            if e.errno == 1049:
                print("Error: Database does not exist, creating database",cfg.mysqldb['database'])
                cnx = mc.connect(host=self.host,user=self.user,password=self.password)
                cursor1 = cnx.cursor()
                sql = "create database {}".format(self.database)
                cursor1.execute(sql)

            elif e.errno == -1:
                print("Error: Check credentials in the database config file")
                print("Exiting...")
                sys.exit(0)
            else:
                print("Error:",e, "Number:",e.errno)
                print("Exiting...")
                sys.exit(0)
        return exists

#------------------------------------------------------------------------
# Create the table exists - if not, create it

    def table_check(self):
        exists = False
        print("in table check")
        try:
            cursor = self.get_cursor()
            sql_string="show tables"
            cursor.execute(sql_string)
            dbtables = cursor.fetchall()
            print("looking for",TABLE_NAME)
            for dbtable in dbtables:
                if dbtable[0] == TABLE_NAME:
                    exists = True
            if not exists:
                # table doesn't exist, create it
                cursor1 = self.get_cursor()
                sql_string1="create table {} (id int AUTO_INCREMENT PRIMARY KEY, title varchar(250), artist varchar(250), year int, genre varchar(250))".format(TABLE_NAME)
                cursor1.execute(sql_string1)
               
        except Error as e:
            print("Error:",e, "Number:",e.errno)
            sys.exit(0)

        return exists

#------------------------------------------------------------------------
# Close the connection and cursor, free up resources

    def close_all(self):
        self.connection.close()
        self.cursor.close()
#------------------------------------------------------------------------

    # Get all records         
    def get_all_records(self):    
        cursor = self.get_cursor()
        sql_string="select * from {}".format(TABLE_NAME)
        cursor.execute(sql_string)

        # results will be a list of database records, each is a list of
        # the fields - so it is a list of lists
        results = cursor.fetchall()
        record_array = []
        for result in results:
            #print(result)
            record_array.append(self.convert_to_dict(result))

        self.close_all()
        return record_array

#------------------------------------------------------------------------
# Find a record by ID

    def find_record_by_id(self, id):
        cursor = self.get_cursor()
        print("retrieving record id =", id)
        sql_string="select * from {} where id = %s".format(TABLE_NAME)
        values = (id,)
        cursor.execute(sql_string, values)
        result = cursor.fetchone()
        returnvalue = self.convert_to_dict(result)
        self.close_all()
        return returnvalue
        #return result
        
#------------------------------------------------------------------------
# Create a record

    def create_record(self, record):

        cursor = self.get_cursor()
        sql_string="insert into {} (title, artist, year, genre) values (%s,%s,%s,%s)".format(TABLE_NAME)
        values = (record.get("title"), record.get("artist"), record.get("year"), record.get("genre"))
        cursor.execute(sql_string, values)
        self.connection.commit()
        new_id = cursor.lastrowid
        record["id"] = new_id
        self.close_all()
        return record

#------------------------------------------------------------------------
    # Update a record with an ID of 'id'

    def update_record(self, id, record):
        cursor = self.get_cursor()
        sql_string="update {} set title= %s,artist=%s, year=%s, genre=%s where id = %s".format(TABLE_NAME)
        print(type(record))
        values = (record.get("title"), record.get("artist"), record.get("year"), record.get("genre"),id)
        cursor.execute(sql_string, values)
        self.connection.commit()
        self.close_all()
        return(record)

#------------------------------------------------------------------------
# Delete a record with an ID of 'id'  

    def delete_record(self, id):
        cursor = self.get_cursor()
        sql_string="delete from {} where id = %s".format(TABLE_NAME)
        values = (id,)
        cursor.execute(sql_string, values)
        self.connection.commit()
        self.close_all()
        print("Deleted record", id)

        return True

#------------------------------------------------------------------------

    def convert_to_dict(self, result_line):
        attkeys=['id','title','artist', "year", "genre"]
        record = {}
        currentkey=0
        for attrib in result_line:
            record[attkeys[currentkey]] = attrib
            currentkey+=1 
        return record

#------------------------------------------------------------------------
# Create an instance of the class 

recordDAO = RecordDAO()
TABLE_NAME = 'records'

# Do some initialization here

# Check if database exists.
recordDAO.db_check()

# check table exists
recordDAO.table_check()

# add a couple of starter records if the table is empty
record = {"title":"London Calling","artist":"The Clash","year":1979,"genre":"Punk"}
record2 = {"title":"Foxtrot","artist":"Genesis","year":1973,"genre":"Rock"}
results = recordDAO.get_all_records()
if not results:
    recordDAO.create_record(record)
    recordDAO.create_record(record2)

# Define a set of tests to execute if this module is run as main 
if __name__ == "__main__":
    record = {"title":"London Calling","artist":"The Clash","year":1979,"genre":"Punk Rock"}
    record2 = {"title":"Foxtrot","artist":"Genesis","year":1973,"genre":"Prog Rock"} 

    print ("test get_all_records()")
    print (f"\t{recordDAO.get_all_records()}")
    print ("test find_record_by_id()")
    print (f"\t{recordDAO.find_record_by_id(2)}")
    print ("test create_record()")
    print (f"\t{recordDAO.create_record(record)}")
    print ("test update_record()")
    print (f"\t{recordDAO.update_record(1,record2)}")
    print ("test delete_record()")
    print (f"\t{recordDAO.delete_record(1)}")