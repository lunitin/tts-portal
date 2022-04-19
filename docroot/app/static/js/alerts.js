/* Automatically dismiss alerts ater 6 seconds */

$(".alert-dismissible")
  .fadeTo(6000, 500)
  .slideUp(500, function() {
    $(".alert-dismissible").alert("close");
  });
