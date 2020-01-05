function submitLogin() {

    var username = $("#username").val();
    var password = $("#password").val();
    // console.log(item_id)

    $.ajax({
        url: "http://localhost:5001/token?username="+username+"&password="+password,
        type: "POST",
        cache: false
    }).done(function (result) {
        console.log("done");
        var jsonResult = JSON.parse(result);
        console.log(jsonResult)
        $.cookie("username", username);
        $.cookie("token", jsonResult);
        window.location="stock.html";
        // $("#update-result").text(jsonResult);
        // $("#update-result").append(result)
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log("fail")
// needs to implement if it fails
    });
}