function submitLogin() {

    var username = $("#username").val();
    var password = $("#password").val();
    // console.log(item_id)
    $("#wrong_login").text("");
    console.log(password)

    $.ajax({
        url: "http://localhost:5001/login",
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
        if(jsonResult === "Permission denied"){
            $("#wrong_login").text("Wrong credentials. Please try again.");
        }else {
            $.cookie("username", username);
            $.cookie("token", jsonResult.token);
            $.cookie("scope", jsonResult.scope)
            window.location="stock.html";
        }

        // $("#update-result").text(jsonResult);
        // $("#update-result").append(result)
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log("fail")
// needs to implement if it fails
    });
}