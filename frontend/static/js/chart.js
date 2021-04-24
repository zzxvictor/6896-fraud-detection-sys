
$( document ).ready(function() {

});

function load_chart(data1, data2){
    const ctx = document.getElementById('histogram').getContext('2d');

    const chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ["Normal Transaction", "Fraud Transaction"],
        datasets: [
            {
                label: 'Correctly Classified',
                data: data1,
                backgroundColor: 'green',
            },
            {
                label: 'Wrongly Classified',
                data: data2,
                backgroundColor: 'red',
            },
        
        ]
      },
      options: {
        datasets: {
            bar: {
                categoryPercentage: 0.8,
                barPercentage: 0.9
            }
        },

        scales: {
          xAxes: [{
            display: false,
            // barPercentage: 1.3,
            ticks: {
              max: 3,
            }
          }, {
            display: true,
            ticks: {
              autoSkip: false,
              max: 4,
            }
          }],
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        }
      }
    });
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }


function check_result(user_id, transaction_id){
    // 0 for genuine
    // 1 for fraud
    console.log("check result!");
    var apigClient = apigClientFactory.newClient();
    console.log(user_id);
    console.log(transaction_id);
    var params = {

        //This is where any header, path, or querystring request params go. The key is the parameter named as defined in the API
        //"user_id": user_id

        // headers: {
        //     "Access-Control-Allow-Origin": "*"
        // },
        // querystring: {
        //     user_id: user_id,
        //     transaction_id: transaction_id
        // }
    };
    var body = {
        //This is where you define the body of the request
        // 'transaction': transaction
        // "user_id": user_id,
        // "transaction_id": transaction_id
    };

    var additionalParams = {
        // "user_id": user_id,
        // "user_id": user_id,
        // "transaction_id": transaction_id
        headers: {
            'Content-Type':"application/json"
        },
        queryParams: {
            "user_id": user_id,
            "transaction_id": transaction_id
        }
    };

    console.log(additionalParams);

    if (user_id == ""){
        alert("You need to enter user id in order to check the result!");
        return;
    }
    if (transaction_id == ""){
        alert("You need to enter transaction id in order to check the result!");
        return;
    }
    
    return apigClient.requestGet(params, body, additionalParams)
            .then(function (result) {
                console.log(result.data);
                //console.log(result.data)
                // var json = JSON.parse(result.data);
                //var status = result.data.statusCode
                //document.getElementById("check_result").innerHTML = json;
                var genuine = parseInt(result.data.genuine);
                var status = result.status;
                console.log(status);

                if (genuine === 1){
                    console.log("GET return 0!");
                    return 0;
                } else {
                    console.log("GET return 1!");
                    return 1;
                }

                // console.log(json.message)
                // //alert(json.message);
                // document.getElementById("response").innerHTML = json.message;
                // if (json.access){
                //     document.getElementById("access").innerHTML = '<img class="small_img" src="static/images/yes.png" alt="Access Approved"><br>';
                // } else {
                //     document.getElementById("access").innerHTML = '<img class="small_img" src="static/images/no.png" alt="Access Denied"><br>';
                // }
                // document.getElementById("response").innerHTML = "Your transaction is received. If there is further issue, we will remind you";
                // document.getElementById("access").innerHTML = '<img class="small_img" src="static/images/yes.png" alt="Access Approved"><br>';
                
            }).catch(function (result) {
            //This is where you would put an error callback
            console.log(result);
            return 1;
        })
        
}

function submit_transaction(headers, transaction){
    var apigClient = apigClientFactory.newClient();
    var params = {
        //This is where any header, path, or querystring request params go. The key is the parameter named as defined in the API
        // 'transaction': transaction,
        // 'headers': headers
    };
    console.log(transaction);
    var body = {
        //This is where you define the body of the request
        'transaction': transaction,
        'headers': headers
    };
    var additionalParams = {
        // 'transaction': transaction,
        // 'headers': headers
    }
    if (transaction == ""){
        alert("You need to enter a piece of transaction information");
    } else {
        apigClient.requestPost(params, body, additionalParams)
            .then(function (result) {
                console.log("Transaction is submit successfully");
                // document.getElementById("access").innerHTML = '<img class="small_img" src="static/images/yes.png" alt="Access Approved"><br>';
                
            }).catch(function (result) {
            //This is where you would put an error callback
            console.log(result);
        });                
    }
}

function preview(event){
    //var files = ("#file").files; // FileList object
    var file = document.getElementById("file").files[0];
    // use the 1st file from the list
    //f = files[0];
    
    var reader = new FileReader();
    // Closure to capture the file information.
    reader.onload = (function(event) {
        $("#content").text(event.target.result);
        // return function(e) {
        //     ("#content").html(e.target.result);
        // };
    });

    // Read in the image file as a data URL.
    reader.readAsText(file);
}

function upload(event){
    var file = document.getElementById("file").files[0];
    // use the 1st file from the list
    //f = files[0];
    $("#content").text("");
    $("#info").text("Uploaded Records");
    var reader = new FileReader();
    // Closure to capture the file information.

    
    reader.onload = (function(event) {
        var lines = event.target.result.split('\n');
        
        var line = 1; // first line is header
        var spinner = document.getElementById("spinner");
        spinner.classList.add("d-flex");
        var spinner2 = document.getElementById("spinner2");
        spinner2.classList.add("d-flex");
        //var arr = new Array();
        var data_correct = new Array(0, 0);
        var data_wrong = new Array(0, 0);
        var interval = setInterval(function() { 
            if (line < lines.length) { 
                // console.log(lines[line]);
                if (!lines[line].includes("|")){
                    console.log("do not have | skip line!");
                    line++;
                    return;
                }
                console.log("headers!");
                console.log(lines[0]);
                
                var words = lines[line].split("|");
                var uid = words[0];
                var tid = words[7];
                
                var label = parseInt(words[10]);
                console.log(label);
                //arr.push([uid, tid, label])
                submit_transaction(lines[0], lines[line]);
                $("#content").append("\n" + lines[line]);

                setTimeout(function () {
                    check_result(uid, tid).then(function(ret){
                        var classify = ret;
                        console.log(classify);

                        if (label == 0){
                            if (classify == 0){
                                data_correct[0] += 1;
                            } else {
                                data_wrong[0] += 1;
                            }
                        } else {
                            if (classify == 0){
                                // wrong
                                data_correct[1] += 1;
                            } else {
                                data_wrong[1] += 1;
                            }
                        }
                        
                        
                        // console.log(data_normal);
                        // console.log(data_fraud);
                        console.log(JSON.stringify(data_correct));
                        console.log(JSON.stringify(data_wrong));
                        load_chart(data_correct, data_wrong);
                    });
                }, 5000);
                
                
                line++;
            }
            else { 
                spinner.classList.remove("d-flex");
                spinner2.classList.remove("d-flex");
                clearInterval(interval);
            }
         }, 500);


        // var spinner2 = document.getElementById("spinner2");
        // spinner2.classList.add("d-flex");
        // var index = 0;
        // data_normal = new Array();
        // data_fraud = new Array();

        // var interval = setInterval(function() { 
        //     if (index < arr.length) { 
        //         //console.log(lines[line]);
        //         var uid = arr[index][0];
        //         var tid = arr[index][1];
        //         var label = parseInt(arr[index][2]);
        //         classify = check_result(uid, tid);
        //         console.log(classify);
        //         if(label === 0){
        //             // genenuine data
        //             if(classify === 0){
        //                 data_normal[0] += 1;
        //             } else {
        //                 data_normal[1] += 1;
        //             }
        //         } else {
        //             if(classify === 0){
        //                 data_fraud[0] += 1;
        //             } else {
        //                 data_fraud[1] += 1;
        //             }
        //         }
        //         console.log(data_normal);
        //         console.log(data_fraud);
        //         load_chart(data_normal, data_fraud);
        //         index++;
        //     }
        //     else { 
        //         spinner2.classList.remove("d-flex");
        //         clearInterval(interval);
        //     }
        //  }, 500);


        // for(var line = 0; line < lines.length; line++){
        //     console.log(lines[line]);
        //     console.log("??????");
        // }
        
    });
    
    
    // Read in the image file as a data URL.
    reader.readAsText(file);
    //spinner.classList.remove("d-flex");
}
