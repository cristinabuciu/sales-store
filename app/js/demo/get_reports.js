$( document ).ready(function() {
    var cookie = $.cookie("username");
    if(cookie == null){
        window.location="login.html";
    }
    $("#useGetReports").text(cookie);
    console.log( cookie );
});

function getStockReport() {
    var username = $.cookie("username")
    var token = $.cookie("token")

    var table = $("#stockReport").DataTable({
        rowCallback: function (row, data) {},
        filter: false,
        info: false,
        ordering: false,
        processing: true,
        retrieve: true
    });

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
            window.location="login.html";
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log("fail")
    });

    $.ajax({
        url: "http://localhost:5002/get-stock-report",
        // url: "data.json",
        type: "GET",
        headers: {
            Accept: "application/json; charset=utf-8",
            "Content-Type": "application/json; charset=utf-8"
        },
        // contentType: "application/json",
        cache: false
    }).done(function (result) {
        var jsonResult = JSON.parse(result);
        if (jsonResult.length === 0) {
            $("#errorMessageStock").text("Empty stock")
        }
        else {
            $("#errorMessageStock").text("")
            table.clear().draw();
            table.rows.add(jsonResult).draw();
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log("fail")
    });
}

function getOrdersReport() {

}

function getUsersReport() {
    var username = $.cookie("username")
    var token = $.cookie("token")

    var table = $("#usersReport").DataTable({
        rowCallback: function (row, data) {},
        filter: false,
        info: false,
        ordering: false,
        processing: true,
        retrieve: true
    });

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
            window.location="login.html";
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log("fail")
    });

    $.ajax({
        url: "http://localhost:5002/get-users-report",
        // url: "data.json",
        type: "GET",
        headers: {
            Accept: "application/json; charset=utf-8",
            "Content-Type": "application/json; charset=utf-8"
        },
        // contentType: "application/json",
        cache: false
    }).done(function (result) {
        var jsonResult = JSON.parse(result);
        if (jsonResult.length === 0) {
            $("#errorMessageStock").text("Empty stock")
        }
        else {
            $("#errorMessageStock").text("")
            table.clear().draw();
            table.rows.add(jsonResult).draw();
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log("fail")
    });
}
