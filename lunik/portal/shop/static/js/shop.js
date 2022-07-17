const params = new URLSearchParams(window.location.search);

$(document).ready(function(){
    $("#order").on("click", ".js-get-order", function (e) {
        e.preventDefault();
        var btn = $(this);
        $.ajax({
          url: btn.attr('data-url'),
          type: 'get',
          dataType: 'json',
          success: function (data) {
            $(".box-order").empty();
            $(".box-order").prepend(data.html_order);
          }
        
        });
        return false;
      });
    /* DESIGNS PRODUCTS CLICK*/
    $(".product-cart").click(function(e){
        e.preventDefault();
        var button = $(this);
        $.ajax({
            url: button.data('url'),
            data: {'product_pk':button.data('product')},
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal_cart").modal("show");
            },
            success: function (data) {
                $("#modal_cart .modal-content").html(data.html_product_cart);
            }
        });
        return false;
    });

    /* ADD PRODUCT TO CART MODAL FORM */
    // $(".detai-product-page").on("submit", ".js-product-form", function () {
    //     var form = $(this);
    //     $.ajax({
    //         url: form.attr("action"),
    //         data: form.serialize(),
    //         type: form.attr("method"),
    //         dataType: 'json',
    //         success: function (data) {
    //             console.log(data)
    //             if (data.form_is_valid) {
                    
    //                 $(".shopping-cart-box").html(data.partial_cart_detail);
    //                 toastr.success("Producto agregado al carrito");
    //                 location.reload();
    //             }
    //             else {
    //                 toastr.error("No se ha podido agregar el producto, intenta de nuevo");
    //             }
    //         }
    //     });
    //     return false;
    // });

    /* UPDATE CART WITH SHIPPING */
    //   $("#id_has_delivery").change(function(){
    //     var shipping_home = $(this).data("shipping-home");
    //     //var shipping_school = $(this).data("shipping-school");
    //     var shipping_limit = $(this).data("shipping-limit");
    //     var shipping_extra = $(this).data("shipping-extra");

    //     if ($(this).val() == "HS"){
    //         _shipping_cost = shipping_home;
    //     }else{
    //         _shipping_cost = 0;
    //     }
    //     $.ajax({
    //         url: $(this).data('url'),
    //         data: {'shipping':_shipping_cost,'limit':shipping_limit,'extra':shipping_extra},
    //         type: 'get',
    //         dataType: 'json',
    //         success: function (data) {
    //             $(".box-cart-partial").html(data.html_cart_checkout);
    //         }
    //     });
    // }).change();

    /* UPDATE PRODUCT FROM CART */
    $(".container-table-cart").on("input", ".update-cart-item",function () {
        this.value = this.value.replace(/[^0-9]/g,"");
    });
    $(".container-table-cart").on("click", ".btn-refresh", function () {
        var btn = $(this);
        var quantity = $("#id_quantity");
        if (quantity.val() > 0 || quantity.val() != ""){

            $.ajax({
                url: btn.data('url'),
                data: {'product_pk':btn.data('product'),'size':btn.data('size'),'quantity':quantity.val()},
                type: 'get',
                dataType: 'json',
                success: function (data) {
                  $('.container-table-cart').html(data.html_cart_table);
                  $(".container-table-coupon").html(data.html_cart_coupon);
                }
            });
            return false;
        }
    });
    // APPLY COUPON
    $('.div-coupon').on('click', '.apply-coupon', function(e){
        e.preventDefault();
        var a = $(this);
        $.ajax({
            url: a.data('url'),
            data: {'coupon': $('#coupon').val()},
            type: 'get',
            dataType: 'json',
            success: function (data) {
                if (!data.coupon_404) {
                    if (data.coupon_is_valid) {
                        toastr.success("Cupon aplicado");
                        $('.cart-table').html(data.html_cart_table);
                        $(".div-total").html(data.html_cart_charge);
                        $(".div-coupon").html(data.html_cart_coupon);
                        
                        // $('#div-coupon').hide()
                    } else if (!data.is_products_in_coupon){
                        // $('#div-coupon').show();
                        toastr.warning("Este cupón no aplica");
                    } else if (!data.min_purchase){
                        // $('#div-coupon').show();
                        toastr.warning(data.min_purchase_msg);

                    } else {
                        // $('#div-coupon').show()
                        toastr.warning("Este cupón ha expirado");
                    } 
                }  else {
                    // $('#div-coupon').show()
                    if (data.coupon_empty){
                      $('#coupon').addClass('is-invalid');
                    } else {
                    toastr.warning("Este cupón no existe.");
                    // toastr.warning("Asegurate que lo hallas escrito bien...");
                    }
                }
            }
        })
    })
    // REMOVE COUPON APPLIED
    $(".div-coupon").on("click",".del-coupon",function(e){
        e.preventDefault();
        var a = $(this);
        $.ajax({
            url: a.data('url'),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $('.cart-table').html(data.html_cart_table);
                    $(".div-total").html(data.html_cart_charge);
                    $(".div-coupon").html(data.html_cart_coupon);
                    toastr.warning("Cupón removido del carrito");
                    // window.location = window.location;
                }
            }
        });
        return false;
    });

    /* ADD/REMOVE GIFT PRODUCT FROM CART */
    $(".container-table-cart").on("click",".gift-item",function(e){
      e.preventDefault();
      var button = $(this);
      $.ajax({
          url: button.data('url'),
          data: {'product':button.data('product'), 'size':button.data('size')},
          type: 'get',
          dataType: 'json',
          success: function (data) {
            if (data.form_is_valid) {
              $(".container-table-cart").html(data.html_cart_table);
              toastr.success(data.message);

            }
          }
      });
      return false;
    });
    /* REMOVE PRODUCT FROM CART DETAIL */
    $(".container-table-cart").on("click",".remove-cart-item",function(e){
        e.preventDefault();
        var button = $(this);
        $.ajax({
            url: button.data('url'),
            data: {'product':button.data('product'),'size':button.data('size'),'checkout':button.data('checkout')},
            type: 'get',
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                  $('.container-table-cart').html(data.html_cart_table);
                  if(data.checkout){
                    if(data.new_quantity == 0){
                      location.reload();
                    } else{
                      toastr.warning("Producto removido del carrito");
                      $(".container-table-coupon").html(data.html_cart_coupon);
                    }
                  } else {
                    if(data.new_quantity == 0){
                      location.reload();
                    } 
                    $('#id-cart-bar').toggleClass('toggled')
                  }
                  $('#quantity_cart').html(data.new_quantity)
                }
            }
        });
        return false;
    });
    /* PICK A DESIGN */
    $(".modal-content").on("click",".pick-design",function(){
        _value = $(this).data("design-selected");
        $("#id_design").val(_value);
		    $(".design-selected").html("");
        $(".design-selected-"+design_pk).html("<i class='fa fa-check'></i>Producto seleccionado");
    });

    /* UPDATE PRODUCT FROM CART */
    $(".modal-dialog").on("input", "#id_quantity",function () {
        this.value = this.value.replace(/[^0-9]/g,"");
    });
    $(".modal-dialog").on("keyup", "#id_quantity", function () {
        var quantity = $(this);
        if ($(this).val() > 1){
            $(".box-personalization").hide();
        }else{
            $(".box-personalization").show();
        }
    });
    /* GET TOTAL QUANTITY OF PRODUCTS */
    function get_total_quantity(){
        var _total = 0;
        $(".update-cart-item").each(function(index){
            _total += parseInt($(this).val());
        });

        return _total;
    }
    $(function () { 
        $('[data-toggle="tooltip"]').tooltip({trigger: 'manual'}).tooltip('show');
      });  
      
      // $( window ).scroll(function() {   
       // if($( window ).scrollTop() > 10){  // scroll down abit and get the action   
        $("#progress-bar").each(function(){
          each_bar_width = $(this).attr('aria-valuenow');
          $(this).width(each_bar_width + '%');
        });
             
       //  }  
      // });
      if(params.has('envio')){
        $("#shipping_free").prop("checked", true);
      }
      if(params.has('oferta')){
        $("#is_sale").prop("checked", true);
      }
      $('#shipping_free').change(function(){
        if($('#shipping_free').is(":checked")){
          addUrlParameter(null,'envio', 'True');
        } else {
          if(params){
            params.delete('envio');
            window.location.search = params.toString()
          }
        }
      });
      $('#is_sale').change(function(){
        if($('#is_sale').is(":checked")){
          addUrlParameter(null,'oferta', 'True');
        } else {
          if(params){
            params.delete('oferta');
            window.location.search = params.toString()
          }
        }
      });
      $('.inputSearch').on('keypress', function(e) {
        //no recuerdo la fuente pero lo recomiendan para
        //mayor compatibilidad entre navegadores.
        var code = (e.keyCode ? e.keyCode : e.which);
        if(code==13){
          if(params.has('buscar')){
            params.delete('buscar');
          }
          params.append('buscar', $(this).val());
          window.location.search = params.toString();
        }
      });
      function hasParams(){
          var total = 0
            params.forEach(function (value,key){
                total += 1
            })
        return total
      }
      if(hasParams() == 0 ){
        $('#iconFilterTrash').css('display', 'none')
       } else {
        $('#iconFilterTrash').removeProp('display')

       }

 });

 function simpleLoad(box, state) {
  if (state) {
      box.toggleClass('sk-loading');
  } else {
      box.toggleClass('sk-loading');
      }
  }

 function sendFormData(){
  var form = $('#form-info');
  $.ajax({
    url: form.attr('action'),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    beforeSend: function () {
      simpleLoad($('#panel_user'),true);

      $('#panel_user').prepend('<div id="loader-bar" class="loader text-center"><span class="bar"></span><span class="bar"></span><span class="bar"></span> </div>');
    },
    success: function (data) {
      simpleLoad($('#panel_user'),false);
      $('#loader-bar').remove();
      if(data.form_is_valid){
        history.pushState({}, null, window.location.origin + '/carrito/checkout/?step='+data.step);
        $(".dynamic-step").html(data.html_dynamic);
        $(".dynamic-footer").html(data.html_footer);
        $(".dynamic-detail").html(data.html_dynamic_detail);
        $(".dynamic-breadcrumb").html(data.html_dynamic_breadcrumb);
        
      } else {
        data.errors.forEach(function (error) {
          console.log(error)
          $('#id_'+error.field).toggleClass('is-invalid')
        })
        toastr.warning('Revisa tus datos de envio y vuelve a intentarlo');
      }
    }
  });
}

 function goStep(elem){
    $.ajax({
        url: elem.data('url'),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          simpleLoad($('#panel_user'),true);
          $('#panel_user').prepend('<div id="loader-bar" class="loader text-center"><span class="bar"></span><span class="bar"></span><span class="bar"></span> </div>');
        },
        success: function (data) {
            // Replace URL with new step
            simpleLoad($('#panel_user'),false);
            $('#loader-bar').remove();
            history.pushState({}, null, window.location.origin + elem.data('url'));
            // Replace HTML with step 
            $(".dynamic-step").html(data.html_dynamic);
            $(".dynamic-footer").html(data.html_footer);
            $(".dynamic-detail").html(data.html_dynamic_detail);
            $(".dynamic-breadcrumb").html(data.html_dynamic_breadcrumb);


        }
    })
}
price_min = parseInt($('#sPriceMin').text());
price_max = parseInt($('#sPriceMax').text());

if ($('#priceMin') && $('#priceMax')){
  if(params.has('min') && params.has('max')){
    params.delete('min', price_min);
    params.delete('max', price_max);
  }
  $('#btnFilterPrice').on('click', function(e){
    e.preventDefault();
    params.append('min', price_min);
    params.append('max', price_max);
    window.location.search = params.toString();
  });
}

// Check if value of parameter exists
function checkValueParamExists(name, value){
  for (const param of params) {
    if(param[0] == name && param[1] == value){
      return true;
    }
  }
  return false;
}

// Add or Remove parameter URL
function addUrlParameter(elem, name, value) {
  if(!checkValueParamExists(name,value)){
    params.append(name, value)
    // elem.addClass('param');
    window.location.search = params.toString()
  } else {
    params.delete(name);
    if(elem != null ) {
      elem.removeClass('param');
    }
    window.location.search = params.toString()
  }
}

function removeAllParams(){
    $.when(
        params.forEach(function (value,key){
            console.log(value, key)
            params.delete(key)
        })
    ).then(function () {
        window.location.search = params.toString()
    });
}

// Send page URL

function sendPage(page){
  return window.location = page
};