# WSAA Final Project - README
README for the WSAA CY24 final project (repository - wsaa_project).  

| Topic | Details |
|---------|-------------|
| **Module:**  | 8640 - Web Services & Applications  |
| **Lecturer:**  | Andrew Beatty  | 
| **Course:**  | Higher Diploma in Science in Computing (Data Analytics)  |
| **Year/Semester:**  | Year 1 / Semester 1  (this is a Year 2 / Semester 1 module) |
| **Student Name:**  | David O'Connell  |
| **Student ID:**  | G00438912  |
| **Student Email:**  | G00438912@atu.ie  |  
   
## Overview
This project implements a database with a catalogue of LP records.
It is accessed through a web front end. The database table is represented in the front end, with the following functionality being supported:  
- Review all entries  
- Create a new entry  
- Update an existing entry  
- Delete an entry  

There are 4 fields that the user can input - title, artist, year and genre. The genre field is a drop down with a fixed list of choices. The fifth field, the id, is assigned by the database and is read-only to the user.  

The code is based on the books server, database and front end implemented by Andrew Beatty during the Web Services and Applications module. New features include:  
- an auto-increment ID assigned by the database and presented as read-only to the user  
- a 'genre' field with a drop-down set of options  
- the table in the HTML page is implemented in condensed format to allow more room for the console or for more page content  
- if the database doesn't exist, it is created  
- if the database table doesn't exist, it is created  
- if the database table is empty on startup, a couple of example records are created  
- selection at startup via command line argument as to whether the server is deployed in localhost or pythonanywhere, with no need for any files to be changed

## How to use

### 1. On pythonanywere

Access the web page with this URL: https://davidoconnell.pythonanywhere.com/recordviewer.html.  
Here is the link to the [GitHub repository](https://github.com/dvdgeroconnell/deploytopythonanywhere.git) - note that this is just for deploying to pythonanywhere, the main project repository if you're deploying locally is in section 2 below.

### 2. In your local python environment

Link to the main [GitHub repository](https://github.com/dvdgeroconnell/wsaa-project).

1. Make a copy of *mysqldbcfg_template.py*, save it as *mysqldbcfg.py* and fill out the credentials in the *local_db* dict.
2. Run the following command in your python environment: *python recordserver.py local*.
    - If the credentials are not correct, the program will terminate and the user will be asked to fix them.
    - If the database specified in *mysqldbcfg.py* does not exist, it will be created.
    - If the *records* table does not already exist in the database, will be created.
    - If the database is empty, it will be populated with a couple of example records.
3. Launch the http://"hostname:port"/recordviewer.html web page.
    - The REST server will tell you on startup the hostname and port to use.
    - Use the web server hosted recordviewer.html rather than one deployed in your file system, as it uses relative paths.

### Schema for *records* table

| Field | Description |
|-------|-------------|
| id | int AUTO_INCREMENT PRIMARY KEY |
| title | varchar(250) |
| artist | varchar(250) |
| year | int |
| genre | varchar(250) |


## Files in this Repository

### README.md
This file. Overview and description of the project, information on how to deploy locally.
### recordserver.py
The flask-hosted web server application.
### recordDAO.py
Data Access Object framework. implements class: RecordDAO.
### staticpages/recordviewer.html
HTML and Javascript front end.
### staticpages/record_ajax.js
Javascript functions with jquery / ajax calls to REST server.
### mysqldbcfg_template.py
The template configuration file. Copy and fill the *local_db* dict out with your host, user, password and database information if deploying locally. Ensure to save the copy as *mysqldbcfg.py*.


## API Definition
The parameters are:

ID - the ID that the program assigns to the entry
Title - the name of the record
Artist - the artist / band featuring on the record
Year - the year the record was released
Genre - The type of music, e.g. Jazz, Rock, Prog, Folk, Punk, Disco

The API will implement the following operations:

| Operation | Method | URL | Sample Parameters | Sample Responses |
|-----------|--------|-----|-------------------|------------------|
| Get All | GET | /records | None | [{...},{...},{...}] |
| Find by ID | GET | /records/id | None | {"id":"1", "Title" : "xxx", |
| | | | | "Artist":"xxx", "Year":1973,|
| | | | | "Genre":"Rock"} |
| Create | POST | /records | {"Title" : "xxx", | {"id":"1", "Title" : "xxx", |
| | | |  "Artist":"xxx", "Year":1973, | "Artist":"xxx", "Year":1973,|
| | | |  "Genre":"Rock"} | "Genre":"Rock"} |
| Update | PUT | /records/id | e.g. {"Year":1970} | {"id":"1", "Title" : "xxx", |
| | | | | "Artist":"xxx", "Year":1970,|
| | | | | "Genre":"Rock"} |
| Delete | DELETE | /records/id | None | {"done":True} |

CURL or Postman may be used to test the server-side functionality.

## Sample CURL commands
Following commands are used with the web server running on localhost. Replace with an appropriate host and port.

### Get All
**local**  
curl -X GET http://127.0.0.1:5000/records  
**pythonanywhere**  
curl -X GET http://davidoconnell.pythonanywhere.com/records  

### Find by ID
1 is just an example, and may need to be changed, depending on what records are in the database.  
Use *Get All* to find out.  
**local**  
curl -X GET http://127.0.0.1:5000/records/1  
**pythonanywhere**  
curl -X GET http://davidoconnell.pythonanywhere.com/records/1  

### Create
**local**  
curl -X POST -H "Content-Type: application/json" -d "{\"title\":\"Close\", \"artist\":\"JoyDivision\", \"year\":1982, \"genre\":\"Other\"}" http://127.0.0.1:5000/records  
**pythonanywhere**  
curl -X POST -H "Content-Type: application/json" -d "{\"title\":\"Close\", \"artist\":\"JoyDivision\", \"year\":1982, \"genre\":\"Other\"}" http://davidoconnell.pythonanywhere.com/records  

### Update
Add the correct ID to end of URL - whatever was returned from 'Create'.  
**local**  
curl -X PUT -H "Content-Type: application/json" -d "{\"title\":\"Closer\", \"artist\":\"Joy Division\", \"year\":1981, \"genre\":\"Other\"}" http://127.0.0.1:5000/records/1  
**pythonanywhere**  
curl -X PUT -H "Content-Type: application/json" -d "{\"title\":\"Closer\", \"artist\":\"Joy Division\", \"year\":1981, \"genre\":\"Other\"}" http://davidoconnell.pythonanywhere.com/records/1  

### Delete
Add the correct ID to end of URL - whatever was returned from 'Create'.  
**local**  
curl -X DELETE http://127.0.0.1:5000/records/1  
**pythonanywhere**  
curl -X DELETE http://davidoconnell.pythonanywhere.com/records/1  


## References
The following sites were consulted frequently during this development.
- https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
- https://www.html.am/html-tutorial/
- https://www.w3schools.com/jsref/default.asp
- https://stackoverflow.com/

****
#### End