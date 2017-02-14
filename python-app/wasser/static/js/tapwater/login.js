$(function () {

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-login").modal("show");
      },
      success: function (data) {
        $("#modal-login .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-login .modal-content").html(data.html_form);
          $('#successMessage').show();
        }
        else {
          $("#modal-login .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  $(".js-create-login").click(loadForm);
  $("#modal-login").on("submit", ".js-login-create-form", saveForm);

});