
$(document).ready(function(){
    $(".alert-message").css("display", "block");  // Show the elements when the page loads
    setTimeout(function() {
        $(".alert-message").fadeOut("slow");  // Hide the elements after 3 seconds
    }, 3000);
}); 
