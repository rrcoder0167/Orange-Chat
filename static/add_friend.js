$(document).ready(function() {
    
    $("#add-friends-button").click(function() {
        $("#popup-window").show();
    });
    $("#close-button").click(function() {
        $("#popup-window").hide();
    });
    $("#friend-email").keypress(function(event) {
        if (event.which == 13) {
            $.post("/search_friends", {search_query: $("#friend-email").val()}, function(data) {
                console.log(data);
                if (data.message == "self_friend_req-error") {
                    $("#search-result").text("Sorry, you can't friend request yourself :(").removeClass().addClass("medium");
                }
                else if (data.success) {
                    $("#search-result").text(data.message).removeClass().addClass("success");
                    $("#search-result").append("<button id='send-friend_req-button'>Send Friend Request</button>");
                    $("#send-friend_req-button").click(function() {
                        $.post("/send_friend_request", {recipient_email: $("#friend-email").val()}, function(data) {
                          console.log(data);
                          $(".sticky-alert-success").text("Success! You sent them a friend request. You'll be accepted :) or rejected ;( in no time").show();
                        }).fail(function(jqXHR, textStatus, errorThrown) {
                          if (jqXHR.status == 400) {
                            console.log("Bad request, sent existing friend request. [ERROR 400]");
                            $(".sticky-alert-warning .sticky-alert-message").text("You already sent them a friend request. Wait for them to accept/reject your request. 'Patience is the key to life' -riddhiman, 2023").parent().show();
                          }
                          if (jqXHR.status == 500) {
                            console.log("Bad request, received existing friend request. [ERROR 500]");
                            $(".sticky-alert-warning .sticky-alert-message").text("You already have a friend request from them. Accept/reject their request first").parent().show();

                          }
                          if (jqXHR.status == 401) {
                            console.log("Bad request, system error. Security vulnerability initiated.[ERROR 401]");
                            $(".sticky-alert-error .sticky-alert-message").text("A system error occurred. Please contact the administrator for assistance.").parent().show();
                          }
                        });
                      });
                }

                else {
                    $("#search-result").text("Sorry, we couldn't find that user.").removeClass().addClass("error");
                }
            });
        }
    });
    $('.accept-friend-request-button').click(function() {
        let friendRequestId = $(this).data('user-id');
        $.ajax({
          url: "/accept_friend_request/" + friendRequestId,
          type: "POST",
          success: function(result) {
            console.log(result);
            // Update the UI to reflect that the friend request has been accepted
          }
        });
      });
      $(".reject-friend-request-button").click(function() {
        var friendRequestId = $(this).data("user-id");
        $.post("/reject_friend_request/" + friendRequestId, function(data) {
          if (data.message === "Friend request rejected.") {
            alert(data.message);
            location.reload();
          } else {
            alert(data.message);
          }
        });
      });
      $(".close-button").click(function() {
        $(this).parent().hide();
      });
});
