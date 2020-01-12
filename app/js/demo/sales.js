$( document ).ready(function() {
    var cookie = $.cookie("username");
    if(cookie == null){
        window.location="login.html";
    }
    $("#userSales").text(cookie);
    console.log( cookie );
});

function submitFormSales() {

    var provider = $("#provider").val();
    var item_name = $("#item_name_2").val();
    var quantity = $("#quantity").val();
    var username = $.cookie("username");
    var token = $.cookie("token");
    // console.log(item_id)

    $.ajax({
        url: "http://192.168.99.124:5001/verify-token",
        // url: "http://localhost:5001/verify-token",
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
        url: "http://192.168.99.124:5000/sales",
        // url: "http://localhost:5000/sales",
        type: "POST",
        headers: {
            Accept: "application/json; charset=utf-8",
            "Content-Type": "application/json; charset=utf-8"
        },
        data: JSON.stringify({
            "provider":provider,
            "item_name":item_name,
            "quantity":quantity,
            "username":username,
            "token":token
        }),
        cache: false
    }).done(function (result) {
        console.log("done");
        var jsonResult = JSON.parse(result);
        $("#update-result").text(jsonResult);
        // $("#update-result").append(result)
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log("fail")
// needs to implement if it fails
    });
}