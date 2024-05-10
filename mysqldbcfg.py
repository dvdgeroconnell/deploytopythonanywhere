# mysqldbcfg.py
#
# Based on the mysqldbcfg_template file, but with database connection
# parameters filled out for both local and remote. The environment is
# chosen at app server startup. 
#
# David O'Connell
#------------------------------------------------------------------------

# local database connection details
local_db = {
    'host':"localhost",
    'user':"root",
    'password':"",
    'database':"wsaa_project"
}

# pythonanywhere connection details
hosted_db = {
    'host':"davidoconnell.mysql.pythonanywhere-services.com",
    'user':"davidoconnell",
    'password':"wsaa123!",
    'database':"davidoconnell$wsaa"
}