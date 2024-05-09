
    var local_url = "http://127.0.0.1:5000/records";
    var andrew_url = "http://andrewbeatty1.pythonanywhere.com/books";
    var relative_url = "/records";

    function getAll(callback) {
        $.ajax({
            "url": local_url,
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

    function getOne(id, callback) {
        $.ajax({
            "url": local_url+"/"+id,
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

    function createRecord(record, callback){
        console.log("record to create: ",JSON.stringify(record));
        $.ajax({
            "url": local_url,
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

    function updateRecord(record, callback){
        console.log("record to update: ",JSON.stringify(record));
        $.ajax({
            "url": local_url+"/"+encodeURI(record.id),
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

    //            THIS VERSION TAKES IN AN ID SEPARATELY 
    //            function updateRecord(record, id, callback){
    //            //console.log(JSON.stringify(book));
    //                $.ajax({
    //                    "url": local_url+"/"+id,
    //                    "method":"PUT",
    //                    "data":JSON.stringify(record),
    //                    "dataType":"JSON",
    //                    contentType:"application/json; charset=utf-8",
    //                    "success":function(result){
    //                        console.log("Updated: ", result);
    //                        callback(result);
    //                    },
    //                    "error":function(xhr,status,error){
    //                        console.log("error: "+status+" msg:"+error);
    //                    }
    //                });
    //            }   

    function deleteRecord(id, callback){
        $.ajax({
            "url": local_url+"/"+id,
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

    // Get All
    function processGetAll(result){
        console.log("in processGetAll");
        for (record of result){
            console.log(record);
            // add it to the local table
            addRecordToTable(record);
        }
    }            

    // Get One
    function processGetOne(result){
        console.log("in processGetOne");
        console.log(result);
        // add it to the local table
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

    // Moved to script tag in html page
    //getAll(processGetAllResponse)

    // TEST CODE

    //getAll(processGetAll);

    //var getid = 2;
    //getOne(getid, processGetOne);

    //record = {"title":"Empires and Dance","artist":"Simple Minds","year":1980,"genre":"Punk"};
    //createRecord(record, processCreateResponse);

    //var updateid = 154;
    //record2 = {"title":"Empires and Dance","artist":"Simple Minds","year":1980,"genre":"Post Punk"};
    //updateRecord(record2, updateid, processUpdateResponse);
    //record3 = {"id":154, "artist":"Jim Kerr"}
    //updateRecord(record3, processUpdateResponse);

    //var deleteid = 179;
    //deleteRecord(deleteid, processDeleteResponse);
