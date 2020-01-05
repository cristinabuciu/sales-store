$( document ).ready(function() {
    var cookie = $.cookie("username");
    $("#userAddStock").text(cookie);
    console.log( cookie );
});
function submitFormAddStock() {

    var provider = $("#provider_add_stock").val();
    var item_name = $("#item_name_add_stock").val();
    var quantity = $("#quantity_add_stock").val();
    var item_id = $("#item_id_add_stock").val();
    var username = $.cookie("username");
    var token = $.cookie("token");

    $.ajax({
        url: "http://localhost:5000/add-stock?item_id="+item_id+"&provider="+provider+"&item_name="+item_name+"&quantity="+quantity,
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
// needs to implement if it fails
    });
}