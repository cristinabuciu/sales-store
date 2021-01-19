$(document).ready(function() {

    var cookie_username = $.cookie("username");
    if(cookie_username == null){
        window.location="login.html";
    }
    $("#userGetReports").text(cookie_username);
    var cookie_scope = $.cookie("scope")
    if (cookie_scope === 'admin') {
        $('#adminMenu').show();
    }
    
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
});

$(function() {
    $('#next').click(function() {
        $('#first').hide();
        $('#second').show();
        var name = $('#name').val();
        var email = $('#mail').val();
        var phone_number = $('#phone-number').val();
        var text=  $('#message').val();
        $.ajax({
            url: "http://localhost:5004/post-message",
            type: "POST",
            headers: {
                Accept: "application/json; charset=utf-8",
                "Content-Type": "application/json; charset=utf-8"
            },
            data: JSON.stringify({
                "name":name,
                "email":email,
                "phone_number": phone_number,
                "message":text
            }),
            cache: false
        }).done(function (result) {
        }).fail(function (jqXHR, textStatus, errorThrown) {
            console.log("fail")
        });
    });
});