# wsaa-project
Repository for the WSAA CY24 final project.

## Overview
This project implements a database of a catalogue of LP records.

## Files in this Repository

#### recordDAOframework.py
DAO framework with a set of stubs for development and test purposes.

#### README.md
This file.

### Latest working versions of files

## How to use

### On PythonAnywere

Access the URL: https://davidoconnell.pythonanywhere.com/recordviewerpa.html

### In your local python environment



If the credentials are not correct, the program will terminate and the user will be asked to fix them.
If the database does not exist, it will be created.
If the records table does not already exist in the database, will be created.
if the database is empty, it will be populated with a couple of records as examples.

create database wsaa_project;
use wsaa_project
create table records (id int AUTO_INCREMENT PRIMARY KEY, title varchar(250), artist varchar(250), year int, genre varchar(250));





#### in WSAA-project
- recordDAO.py - the database DAO.
- record_rest_srv_cors.py - the flask app server with CORS changes. Also reinstated the convert to dict code.
- recordviewer4.html - adding genre. Replaces recordviewer3.html.
- record_ajax2.js - adding genre.
#### in WSAA-coursework
- testGetAll.html - equivalent of lab0603 (Ajax). Known good working copy. Moved wip version to WSAA-project.

### Older retained files
- recordviewer.html - original version of the html / Javascript file
- recordviewer2.html - updated, known good working copy with HTML and Javascript
- recordviewer3.html - Database udpdates working. Replaces recordviewer2.html.
- record_rest_srv.py - before CORS and other changes.
- testGetAll2.html - working copy.
- record_ajax.js - javascript functions with ajax calls.


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

As the program will be implemented in stages, curl will be used to test the server-side functionality.

### Sample CURL commands
Following commands are used with the web server running on localhost.

#### Get All
curl -X GET http://127.0.0.1:5000/records

#### Find by ID
5 is just an example, and can be changed.
curl -X GET http://127.0.0.1:5000/records/5

#### Create
curl -X POST -H "Content-Type: application/json" -d "{\"title\":\"Closer\", \"artist\":\"Joy Division\", \"year\":1981, \"genre\":\"post punk\"}" http://127.0.0.1:5000/records

#### Update
curl -X PUT -H "Content-Type: application/json" -d "{\"title\":\"Further\"}" http://127.0.0.1:5000/records/5

#### Delete 
curl -X DELETE http://127.0.0.1:5000/records/5


## References
https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
