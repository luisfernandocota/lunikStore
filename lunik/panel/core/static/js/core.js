$(document).ready(function () {
  $(".cmodal").on("click", ".show-modal", function (e) {
    var btn = $(this);
    $.ajax({
      url: btn.attr('data-url'),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#inlineForm").modal("show");
      },
      success: function (data) {
        $("#inlineForm .modal-content").html(data.html_form);
      }
    });
  });

  $("#inlineForm").on("submit", ".submit-form", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#inlineForm .modal-content").html(data.html_success);
        } else {

          $("#inlineForm .modal-content").html(data.html_failed);
        }
      }
    });
    return false;
  });
  $("#inlineForm").on("submit", ".confirm-form", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          window.location = data.url_redirect
        } else {

          $("#inlineForm .modal-content").html(data.html_failed);
        }
      }
    });
    return false;
  });
  /* DELETE MODAL CLICK*/
  $(".wrapper-content").on("click", ".js-view-delete", function () {
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

  /* SENDMAIL MODAL CLICK*/
  $(".table_list").on("click", ".js-send-activation", function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr('data-url'),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-box").modal("show");
      },
      success: function (data) {
        $("#modal-box .modal-content").html(data.html_sendmail);
      }
    });
  });

  /* SENDMAIL MODAL FORM */
  $("#form_sendmail").on("submit", ".js-sendmail-form", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          toastr.success("Correo enviado correctamente");
          $("#modal-box").modal("hide");  // <-- Close the modal
          if (data.url_redirect) {
            window.location = data.url_redirect
          }
        }
        else {
          $("#modal-box .modal-content").html(data.html_sendmail);
        }
      }
    });
    return false;
  });

  /* DELETE MODAL FORM */
  $("#modal-box").on("submit", ".js-delete-form", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          if (data.edit) {
            toastr.success("Registro editado correctamente");
          } else {
            toastr.success("Registro eliminado correctamente");
          }
          $("#modal-box").modal("hide");  // <-- Close the modal
          if (data.url_redirect) {
            window.location = data.url_redirect
          } else {
            $("#box_" + data.obj_pk + "").remove();
          }
        }
        else {
          $("#modal-box .modal-content").html(data.html_delete);
        }
      }
    });
    return false;
  });

  /* ITEM MODAL CLICK */
  $(".js-item-delete").click(function (e) {
    e.preventDefault();
    var btn = $(this);
    $.ajax({
      url: btn.attr('data-url') + "" + btn.attr('data-id'),
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
  $(".js-item-edit").click(function (e) {
    e.preventDefault();
    var btn = $(this);
    $.ajax({
      url: btn.attr('data-url') + "" + btn.attr('data-id'),
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
  /* GALLERY NEW FORM */
  // $('.gallery-formset').formset({
  //   prefix: 'gallery',
  //   addText: 'Agregar',
  //   deleteText: 'Eliminar'
  // });

  /* USER ROLE SELECTED*/
  $("#wizard").on("change", "#id_role", function () {
    var _value = $(this).val();
    if (_value != "") {
      $.ajax({
        url: $("input[name=usertype_select]").data("url"),
        data: { 'role': _value },
        type: 'get',
        dataType: 'json',
        success: function (data) {
          $("input[name=usertype_select]").val(data.is_group);
        }
      });
    } else {
      $("input[name=usertype_select]").val("");
    }
  });
});

