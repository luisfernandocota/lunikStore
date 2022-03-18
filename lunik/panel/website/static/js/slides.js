$(document).ready(function() {
  /* MODAL SLIDE FORM */
  $("#modal-box").on("submit", ".js-slide-form", function (e) {
    e.preventDefault();
    var form = $(this);
    var formData = new FormData(this);
    $.ajax({
      url: form.attr("action"),
      data: formData,
      type: form.attr("method"),
      contentType: false,
      processData: false,
      success: function (data) {
        console.log(data)
        if (data.form_is_valid) {
          if(data.edit){
            toastr.success("Registro editado correctamente");
          } else {
          toastr.success("Registro eliminado correctamente");
          }
          $("#modal-box").modal("hide");  // <-- Close the modal
          if (data.url_redirect){
            window.location = data.url_redirect
          }else{
            $("#box_"+data.obj_pk+"").remove();
          }
        }
        else {
          $("#modal-box .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  });

    /* ITEM MODAL CLICK */ 
    $(".js-item").click(function (e) {
        e.preventDefault();
        var btn = $(this);
        $.ajax({
          url: btn.attr('data-url'),
          type: 'get',
          dataType: 'json',
          beforeSend: function () {
            $("#modal-box").modal("show");
          },
          success: function (data) {
            $("#modal-box .modal-content").html(data.html_form);
          }
        });
      });

})