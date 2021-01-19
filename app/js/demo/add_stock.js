$( document ).ready(function() {
    var cookie_username = $.cookie("username");
    if(cookie_username === null){
        window.location="login.html";
    }
    $("#userAddStock").text(cookie_username);
    var cookie_scope = $.cookie("scope")
    if (cookie_scope === 'admin') {
        $('#adminMenu').show();
    }
});

function submitFormAddStock() {

    var provider = $("#provider_add_stock").val();
    var item_name = $("#item_name_add_stock").val();
    var quantity = $("#quantity_add_stock").val();
    var item_id = $("#item_id_add_stock").val();
    var username = $.cookie("username");
    var token = $.cookie("token");

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
        // url: "http://192.168.99.124:5000/add-stock",
        url: "http://localhost:5000/add-stock",
        type: "POST",
        headers: {
            Accept: "application/json; charset=utf-8",
            "Content-Type": "application/json; charset=utf-8"
        },
        data: JSON.stringify({
            "provider":provider,
            "item_name":item_name,
            "item_id":item_id,
            "quantity":quantity,
            "username":username,
            "token":token
        }),
        cache: false
    }).done(function (result) {
        console.log("done");
        var jsonResult = JSON.parse(result);
        $("#update_result_add_stock").text(jsonResult);
        // $("#update-result").append(result)
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log("fail")
    });
}