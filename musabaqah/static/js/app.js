document.addEventListener("DOMContentLoaded", function() {
    // Message/Notification timer
    var message_timeout = document.getElementById("message-timer");
  
    if (message_timeout) {
      setTimeout(function() {
        message_timeout.style.display = "none";
      }, 5000); // Hide after 5 seconds
    }
  });
  