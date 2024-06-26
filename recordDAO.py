# recordDAO.py
#
# This file implements the Data Access Object used by recordserver.py
# for all operations. It implements the following:
# 1) Get all records
# 2) Get one record by ID
# 3) Create a record
# 4) Update a record
# 5) Delete a record
# 
# David O'Connell
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
# Init with different config if running locally versus on pythonanywhere

    def __init__(self):

        local_dao = False

        if (len(sys.argv)) > 1:
            local = sys.argv[1]
            if local == "local":
                local_dao = True
                print("DAO Running local app server instance")

        # For anything other than "local"...
        if not local_dao:
            print("DAO Running pythonanywhere app server instance")

        if local_dao:
            self.host     = cfg.local_db['host']
            self.user     = cfg.local_db['user']
            self.password = cfg.local_db['password']
            self.database = cfg.local_db['database']
        else:
            self.host     = cfg.hosted_db['host']
            self.user     = cfg.hosted_db['user']
            self.password = cfg.hosted_db['password']
            self.database = cfg.hosted_db['database']         

#------------------------------------------------------------------------
# Function to create a database connection and return a cursor

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
# Function to check if the database from the configuration file exists

    def db_check(self):
        exists = False
        try:
            print("Looking for", self.database)
            # This won't return a cursor if the database doesn't exist, exception will be thrown
            cursor = self.get_cursor()
            if cursor:
                exists = True
        except Error as e:
            if e.errno == 1049:
                # This is the error we get if the specificed database can't be found
                print("Error: Database does not exist, creating database",self.database)
                cnx = mc.connect(host=self.host,user=self.user,password=self.password)
                cursor1 = cnx.cursor()
                sql = "create database {}".format(self.database)
                cursor1.execute(sql)

            elif e.errno == -1:
                # This is the error we get if the credentials are incorrect
                print("Error: Check credentials in the database config file")
                print("Exiting...")
                sys.exit(0)
            else:
                # Print the error number and stop the program as we won't be able to proceed
                print("Error:",e, "Number:",e.errno)
                print("Exiting...")
                sys.exit(0)
        return exists

#------------------------------------------------------------------------
# Create the table exists - if not, create it

    def table_check(self):
        exists = False
        #print("in table check")
        try:
            cursor = self.get_cursor()
            sql_string="show tables"
            cursor.execute(sql_string)
            dbtables = cursor.fetchall()
            #print("looking for",TABLE_NAME)
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
# Get all records from the database, returns a list of dicts

    def get_all_records(self):
  
        cursor = self.get_cursor()
        sql_string="select * from {}".format(TABLE_NAME)
        cursor.execute(sql_string)

        # results will be a list of database records, each is a list of
        # the fields, converted to dict
        results = cursor.fetchall()
        record_array = []
        for result in results:
            record_array.append(self.convert_to_dict(result))
        self.close_all()

        return record_array

#------------------------------------------------------------------------
# Find and return a record by ID.

    def find_record_by_id(self, id):

        cursor = self.get_cursor()
        #print("retrieving record id =", id)
        sql_string="select * from {} where id = %s".format(TABLE_NAME)
        values = (id,)
        cursor.execute(sql_string, values)
        result = cursor.fetchone()

        # Convert to dict
        returnvalue = self.convert_to_dict(result)
        self.close_all()

        return returnvalue
        
#------------------------------------------------------------------------
# Create a record in the database

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
        values = (record.get("title"), record.get("artist"), record.get("year"), record.get("genre"),id)
        cursor.execute(sql_string, values)
        self.connection.commit()
        self.close_all()

        return record

#------------------------------------------------------------------------
# Delete a record with an ID of 'id'  

    def delete_record(self, id):

        cursor = self.get_cursor()
        sql_string="delete from {} where id = %s".format(TABLE_NAME)
        values = (id,)
        cursor.execute(sql_string, values)
        self.connection.commit()
        #print("Deleted record", id)
        self.close_all()

        return True

#------------------------------------------------------------------------
# Function to convert a list of attributes into a dict for easier handling

    def convert_to_dict(self, result_line):

        attkeys=['id','title','artist', "year", "genre"]
        record = {}
        currentkey=0
        for attrib in result_line:
            record[attkeys[currentkey]] = attrib
            currentkey+=1 

        return record

#------------------------------------------------------------------------
# Create an instance of the Record DAO() class 

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
    find_id = input("Enter an ID to find: ")
    print (f"\t{recordDAO.find_record_by_id(find_id)}")
    print ("test create_record()")
    print (f"\t{recordDAO.create_record(record)}")
    print ("test update_record()")
    upd_id = input("Enter an ID to update (update is fixed): ")
    print (f"\t{recordDAO.update_record(upd_id,record2)}")
    print ("test delete_record()")
    del_id = input("Enter an ID to delete: ")
    print (f"\t{recordDAO.delete_record(del_id)}")