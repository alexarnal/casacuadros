// JavaScript Document
$(document).ready(function() {
  const lockModal = $("#lock-modal");
  const loadingCircle = $("#loading-circle");
  const form = $("#fs-frm");


  form.on('submit', function(e) {
    e.preventDefault(); //prevent form from submitting

    //const firstname = $("input[name=user_firstname]").val();
    //const lastname = $("input[name=user_lastname]").val();

    // lock down the form
    lockModal.css("display", "block");
    loadingCircle.css("display", "block");

    form.children("input").each(function() {
      $(this).attr("readonly", true);
    });


    e.currentTarget.submit();/*(function() {
      // re-enable the form
      lockModal.css("display", "none");
      loadingCircle.css("display", "none");

      form.children("input").each(function() {
        $(this).attr("readonly", false);
      });

      
    });*/
  });

});