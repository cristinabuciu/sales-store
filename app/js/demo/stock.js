 $( document ).ready(function() {
    var cookie_username = $.cookie("username");
    if(cookie_username == null){
        window.location="login.html";
    }
    $("#userStock").text(cookie_username);
    var cookie_scope = $.cookie("scope")
    if (cookie_scope === 'admin') {
        $('#adminMenu').show();
    }
});

function submitForm() {
    var table = $("#dataTable").DataTable({
        rowCallback: function (row, data) {},
        filter: false,
        info: false,
        ordering: false,
        processing: true,
        retrieve: true
    });

    var item_id = $("#item_id").val()
    var item_name = $("#item_name").val()
    var username = $.cookie("username")
    var token = $.cookie("token")
    console.log(item_id)

    $.ajax({
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
        // url: "http://192.168.99.124:5000/stock",
        url: "http://localhost:5000/get-stock",
        // url: "data.json",
        type: "POST",
        headers: {
            Accept: "application/json; charset=utf-8",
            "Content-Type": "application/json; charset=utf-8"
        },
        data: JSON.stringify({
            "item_id":item_id,
            "item_name":item_name,
            "username":username,
            "token":token
        }),
        // contentType: "application/json",
        cache: false
    }).done(function (result) {
        console.log("done");
        var jsonResult = JSON.parse(result);
        console.log(jsonResult);
        if (jsonResult.length === 0) {
            $("#errorMessageStock").text("Selected item is not in stock. Please try another product.")
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