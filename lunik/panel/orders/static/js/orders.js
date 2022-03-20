$(document).ready(function() {

  /* SEARCH ORDERS/CAMPAIGNS */
  $(".card-header").on("submit", ".js-search-form", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      beforeSend: function(){
        $("#box_orders_loading").children(".ibox-content").toggleClass("sk-loading");
      },
      success: function (data) {
        console.log(data)
        $("#box_orders_loading").children(".ibox-content").toggleClass("sk-loading");
        if (data.search_valid) {
          $(".orders_list").empty();
          $(".orders_list").append(data.html_orders);
          feather.replace();

        }else{
          toastr.error(data.message);
        }
      }
    });
    return false;
  });

  /* SHOP ADDRESS MODAL CLICK*/
  $(".table_list").on("click", ".js-shop-address", function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr('data-url'),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-box").modal("show");
      },
      success: function (data) {
        $("#modal-box .modal-content").html(data.html_order_delivery);
      }
    });
    return false;
  });

  $('#loading-campaigns').click(function () {
    btn = $(this);
    simpleLoad(btn, true)
    window.location = "/panel/orders/";
    simpleLoad(btn, false)
  });
  function simpleLoad(btn, state) {
    if (state) {
        btn.children().addClass('fa-spin');
        btn.contents().last().replaceWith(" Cargando");
    } else {
        setTimeout(function () {
            btn.children().removeClass('fa-spin');
            btn.contents().last().replaceWith(" Actualizar");
        }, 2000);
        }
    }
});