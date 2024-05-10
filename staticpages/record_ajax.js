// recordajax.js

//This is the javascript code with ajax calls to access the REST server methods
// via HTTP.
 
// David O'Connell
//------------------------------------------------------------------------
    
var local_url = "http://127.0.0.1:5000/records";
var relative_url = "/records";

//------------------------------------------------------------------------
// Retrieve all records from the database

function getAll(callback) {
    $.ajax({
        "url": relative_url,
        "method":"GET",
        "data":"",
        "dataType": "JSON",
        "success":function(result){
            console.log("result is :", result);
            callback(result);
        },
        "error":function(xhr,status,error){
            console.log("error: "+status+" msg:"+error);
        }
    });
}

//------------------------------------------------------------------------
// Retrieve one record from the database

function getOne(id, callback) {
    $.ajax({
        "url": relative_url+"/"+id,
        "method":"GET",
        "data":"",
        "dataType": "JSON",
        "success":function(result){
            console.log("result is :", result);
            callback(result);
        },
        "error":function(xhr,status,error){
            console.log("error: "+status+" msg:"+error);
        }
    });
}

//------------------------------------------------------------------------
// Create a record in the database

function createRecord(record, callback){
    console.log("record to create: ",JSON.stringify(record));
    $.ajax({
        "url": relative_url,
        "method":"POST",
        "data":JSON.stringify(record),
        "dataType":"JSON",
        contentType:"application/json; charset=utf-8",
        "success":function(result){
            console.log("Created: ", result);
            callback(result);
        },
        "error":function(xhr,status,error){
            console.log("error: "+status+" msg:"+error);
        }
    });
}

//------------------------------------------------------------------------
// Update a record in the database

function updateRecord(record, callback){
    console.log("record to update: ",JSON.stringify(record));
    $.ajax({
        "url": relative_url+"/"+encodeURI(record.id),
        "method":"PUT",
        "data":JSON.stringify(record),
        "dataType":"JSON",
        contentType:"application/json; charset=utf-8",
        "success":function(result){
            console.log("Updated: ", result);
            callback(result);
        },
        "error":function(xhr,status,error){
            console.log("error: "+status+" msg:"+error);
        }
    });
}

//------------------------------------------------------------------------
// Delete a record from the database

function deleteRecord(id, callback){
    $.ajax({
        "url": relative_url+"/"+id,
        "method":"DELETE",
        "data":"",
        "dataType":"JSON",
        contentType:"application/json; charset=utf-8",
        "success":function(result){
            console.log(result);
            callback(result);
        },
        "error":function(xhr,status,error){
            console.log("error: "+status+" msg:"+error);
        }
    });
}

//------------------------------------------------------------------------
// Callback functions
//------------------------------------------------------------------------

// Get All
function processGetAll(result){
    console.log("in processGetAll");
    for (record of result){
        console.log(record);
        // add it to the browser table
        addRecordToTable(record);
    }
}            

// Get One
function processGetOne(result){
    console.log("in processGetOne");
    console.log(result);
    // add it to the browser table
    addRecordToTable(result);
}

// Create
function processCreateResponse(result){
    console.log("in process create");
    console.log(result);
    addRecordToTable(result)
}

// Update
function processUpdateResponse(result){
    console.log("in process update");
    console.log(result);
}

// Delete
function processDeleteResponse(result){
    console.log("in process delete");
    console.log(result);
}