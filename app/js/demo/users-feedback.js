$(document).ready(function() {
    var cookie = $.cookie("username");
    if(cookie == null){
        window.location="login.html";
    }
    var username = $.cookie("username")
    var token = $.cookie("token")
    $.ajax({
        // url: "http://192.168.99.124:5001/verify-token",
        url: "http://localhost:5001/verify-token",
        type: "POST",
        headers: {
            Accept: "application/json; charset=utf-8",
            "Content-Type": "application/json; charset=utf-8"
        },
        data: JSON.stringify({
            "username":username,
            "token":token
        }),
        cache: false
    }).done(function (result) {
        var jsonResult = JSON.parse(result);
        if(jsonResult == "access-denied"){
            $.removeCookie("username");
            $.removeCookie("token");
            $.removeCookie("scope");
            window.location="login.html";
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log("fail")
    });
    $.ajax({
        url: "http://localhost:5004/get-messages",
        type: "GET",
        headers: {
            Accept: "application/json; charset=utf-8",
            "Content-Type": "application/json; charset=utf-8"
        },
        cache: false
    }).done(function (result) {
        var table = $("#dataTable").DataTable({
            rowCallback: function (row, data) {},
            filter: false,
            info: false,
            ordering: false,
            processing: true,
            retrieve: true
        });
        console.log(JSON.parse(result))
        table.clear().draw();
        table.rows.add(JSON.parse(result)).draw();
        
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log("fail")
    });
    
});