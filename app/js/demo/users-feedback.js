$(document).ready(function() {
    var username = $.cookie("username");
    if(username == null){
        window.location="login.html";
    }
    $("#usersFeedback").text(username);
    var token = $.cookie("token")
    var cookie_scope = $.cookie("scope")
    if (cookie_scope !== 'admin') {
        alert('No admin!' + cookie_scope + ' ' + cookie_username)
        window.location="login.html";
    }
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

            alert('Access denied!' + username + ' ' + token)
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