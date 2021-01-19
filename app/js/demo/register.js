function submitRegister() {

    var username = $("#registerUsername").val();
    var password = $("#registerInputPassword").val();
    // console.log(item_id)
    $("#wrong_register").text("");

    console.log("register")
    console.log(password)
    console.log(password)

    $.ajax({
        url: "http://localhost:5001/register",
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
            $("#wrong_register").text("Something went wrong, please retry.");
        }else {
            window.location="login.html";
        }

    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log("fail")
// needs to implement if it fails
    });
}