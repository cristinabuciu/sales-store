$(document).ready(function() {

    var username = $.cookie("username");
    if(username == null){
        window.location="login.html";
    }
    $("#usersRecommendation").text(username);
    $("#ex2").slider({});
    var cookie_scope = $.cookie("scope")
    if (cookie_scope === 'admin') {
        $('#adminMenu').show();
    } else {
        $('#displayUser').show();
    }
    var token = $.cookie("token");

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
        url: "http://localhost:5005/get-providers",
        type: "GET",
        headers: {
            Accept: "application/json; charset=utf-8",
            "Content-Type": "application/json; charset=utf-8"
        },
        cache: false
    }).done(function (result) {
        var jsonResult = JSON.parse(result);
        console.log(jsonResult);
        var text = "<option selected>Choose...</option> <br>";
        for( var i = 0; i < jsonResult.length; i++) {
            text += " <option value=\"" + jsonResult[i] + "\">" + jsonResult[i] +"</option> <br>"
        }
        console.log(text);
        $("#inputGroupSelect02").html(text);

    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.log("fail")
    // needs to implement if it fails
    });
});

$('#showRecommendations').click(function() {
    var table = $("#dataTable").DataTable({
        rowCallback: function (row, data) {},
        filter: false,
        info: false,
        ordering: false,
        processing: true,
        retrieve: true
    });

    var username = $.cookie("username");
    $.ajax({
        url: "http://localhost:5005/get-recommendation",
        type: "POST",
        headers: {
            Accept: "application/json; charset=utf-8",
            "Content-Type": "application/json; charset=utf-8"
        },
        data: JSON.stringify({
            "username":username
        }),
        cache: false
    }).done(function (result) {
        console.log(result)
        var jsonResult = JSON.parse(result);
        table.clear().draw();
        table.rows.add(jsonResult).draw();
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

    $( "#slider-range" ).slider({
        range: true,
        min: 10,
        max: 10000,
        values: [ 200, 500 ],
        slide: function( event, ui ) {
          $( "#amount" ).val(ui.values[ 0 ] + " - " + ui.values[ 1 ] );
        }
      });
      $( "#amount" ).val( $( "#slider-range" ).slider( "values", 0 ) +
        " - " + $( "#slider-range" ).slider( "values", 1 ) );
  
    
    $('#showCustomRecommendations').click(function() {

        var table2 = $("#dataTable2").DataTable({
            rowCallback: function (row, data) {},
            filter: false,
            info: false,
            ordering: false,
            processing: true,
            retrieve: true
        });

        var provider = $('#inputGroupSelect02').val();
        var selected_vals = $('#ex2').val().split(',');
        var min_val = selected_vals[0];
        var max_val = selected_vals[1];

        $.ajax({
            url: "http://localhost:5005/get-custom-recommendation",
            type: "POST",
            headers: {
                Accept: "application/json; charset=utf-8",
                "Content-Type": "application/json; charset=utf-8"
            },
            data: JSON.stringify({
                "provider" : provider,
                "min_val" : min_val,
                "max_val" : max_val
            }),
            cache: false
        }).done(function (result) {
            console.log(result)
            var jsonResult = JSON.parse(result);
            table2.clear().draw();
            table2.rows.add(jsonResult).draw();
        }).fail(function (jqXHR, textStatus, errorThrown) {
            console.log("fail")
        });
    });
});