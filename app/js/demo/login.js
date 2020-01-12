function submitLogin() {

    var username = $("#username").val();
    var password = $("#password").val();
    // console.log(item_id)
    $("#wrong_login").text("");

    $.ajax({
        url: "http://192.168.99.124:5001/token",
        // url: "http://localhost:5001/token",
        type: "POST",
        headers: {
            Accept: "application/json; charset=utf-8",
            "Content-Type": "application/json; charset=utf-8"
        },
        data: JSON.stringify({
            "username":username,
            "password":password
        }),
        cache: false
    }).done(function (result) {
        console.log("done");
        var jsonResult = JSON.parse(result);
        console.log(jsonResult)
        if(jsonResult == "Permission denied"){
            $("#wrong_login").text("Wrong credentials. Please try again.");
        }else {
            $.cookie("username", username);
            $.cookie("token", jsonResult);
            window.location="stock.html";
        }

        // $("#update-result").text(jsonResult);
        // $("#update-result").append(result)
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log("fail")
// needs to implement if it fails
    });
}