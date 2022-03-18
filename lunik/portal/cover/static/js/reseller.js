$(document).ready(function() {
    function simpleLoad(box, state) {
        if (state) {
          box.toggleClass('sk-loading');
        } else {
          box.toggleClass('sk-loading');
            }
        }
    $('#formulario').prepend("<div class='sk-spinner sk-spinner-three-bounce'><div class='sk-bounce1'></div><div class='sk-bounce2'></div><div class='sk-bounce3'></div></div>");    /* SAVE MODAL FORM RESELLER */
    $(".div-form").on("submit", ".js-reseller-form", function () {
        var form = $(this);
        simpleLoad($('#formulario'), true);
        $.ajax({
          url: form.attr("action"),
          data: form.serialize(),
          type: form.attr("method"),
          dataType: 'json',
          success: function (data) {
            simpleLoad($('#formulario'), false);
            if (data.form_is_valid) {
              $(".formularioItem").html(data.html_form);
            }
            else {

              if(data.result){console.log(data.result)}
              $(".formularioItem").html(data.html_form);
              if(data.director_404){
                $("#code").parent().addClass('form-control.error');
                $("#code").addClass('errormsg');
                $("#code").after("<span class='help-block text-danger'>Director no encontrado...</span>");
              }
            }
          }
        });
        return false;
      });
});