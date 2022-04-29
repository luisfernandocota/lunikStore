$(document).ready(function() {
  function simpleLoad(box, state) {
    if (state) {
        box.toggleClass('sk-loading');
    } else {
        box.toggleClass('sk-loading');
        }
    }
  $("input:checkbox").on('click', function() {

    // in the handler, 'this' refers to the box clicked on
    var $box = $(this);
    if ($box.is(":checked")) {
      // the name of the box is retrieved using the .attr() method
      // as it is assumed and expected to be immutable
      var group = "input:checkbox[name='" + $box.attr("name") + "']";
      // the checked state of the group/box on the other hand will change
      // and the current value is retrieved using .prop() method
      $(group).prop("checked", false);
      $box.prop("checked", true);
    } else {
      $box.prop("checked", false);
    }
  });

  $('.filter-checkbox').change(function() {
    let checkFilters = new Array();
    var checkbox = $(this);
    var pending = $('#pending').is(':checked'); 
    var process = $('#process').is(':checked'); 
    var send = $('#send').is(':checked'); 
    var delivered = $('#delivered').is(':checked'); 
    var canceled = $('#canceled').is(':checked');

    checkFilters.push({
      pending : pending,
      process : process, 
      send : send,
      delivered : delivered,
      canceled : canceled
    })

      $.ajax({
        url: checkbox.attr('data-url'),
        data: {'pending':pending, 'process':process, 'send':send, 'delivered':delivered, 'canceled':canceled},
        type: 'get',
        dataType: 'json',
        beforeSend: function(){
          simpleLoad($('#box-content'), true);
          console.log($('#box-content'))
          $('#box-content').prepend("<div class='sk-spinner sk-spinner-three-bounce'><div class='sk-bounce1'></div><div class='sk-bounce2'></div><div class='sk-bounce3'></div></div>");
        },
        success: function (data) {
          simpleLoad($('#box-content'), false);

          if (data.search_valid) {
            $(".orders-list").empty();
            $(".orders-list").append(data.html_orders);
            feather.replace();
  
          }else{
            toastr.error(data.message);
          }
        }
      });

  });
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