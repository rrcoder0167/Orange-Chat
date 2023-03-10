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
                        $.post("/send_friend_request", {receiver_email: $("#friend-email").val()}, function(data) {
                          console.log(data);
                          $(".sticky-alert-success .sticky-alert-message").text("Success! You sent them a friend request. You'll be accepted :) or rejected ;( in no time").parent().show();
                          $("#pending-friend-requests").append(`
                              <li id="friend-request-${data.id}">${data.username}
                                  <button class="cancel-friend-req-btn" data-friend-request-id="${data.id}">Cancel</button>
                              </li>
                          `);
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
    $(".accept-friend-req-btn").click(function() {
        var friendRequestId = $(this).data("friend-request-id");
        $.post("/accept_friend_request", {friend_request_id: friendRequestId}, function(data) {
            if (data.message == "accept_friend_request-success") {
              // Remove the friend request from the list on the page
              $("#friend-request-" + friendRequestId).remove();
              $("#friend-" + data.friend_request_id).add();
            } else {
              console.error("Error accepting friend request: " + data.message);
            }
          });
      });
      $(".decline-friend-req-btn").click(function() {
        var friendRequestId = $(this).data("friend-request-id");
        console.log(friendRequestId);
        $.post("/decline_friend_request", {friend_request_id: friendRequestId}, function(data) {
            if (data.message == "decline_friend_request-success") {
              // Remove the friend request from the list on the page
              $("#friend-request-" + friendRequestId).remove();
            } else {
              console.error("Error cancelling friend request: " + data.message);
            }
          });
      });
      $(".close-button").click(function() {
        $(this).parent().hide();
      });
      $(".cancel-friend-req-btn").click(function() {
        var friendRequestId = $(this).data("friend-request-id");
        console.log(friendRequestId)
        $.post("/cancel_friend_request", {friend_request_id: friendRequestId}, function(data) {
            if (data.message == "cancel_friend_request-success") {
              // Remove the friend request from the list on the page
              $("#friend-request-" + friendRequestId).remove();
              // Add the flash message to the page
              $("#flash-messages").append("<div class='alert-success alert-message'>" + data.flash_message + "</div>");
            } else {
              console.error("Error cancelling friend request: " + data.message);
            }
          });
      });

});
