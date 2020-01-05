$( document ).ready(function() {
    var cookie = $.cookie("username");
    $("#userStock").text(cookie);
    console.log( cookie );
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
        url: "http://localhost:5000/stock?item_id="+item_id+"&item_name="+item_name,
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