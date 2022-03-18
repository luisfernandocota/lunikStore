$(document).ready(function() {

  var flag_b_m = false;
  var flag_b_y = false;
  var flag = false;
  var flag_e_m = false;
  var flag_e_y = false;
  function simpleLoad(box, state) {
    if (state) {
      box.toggleClass('sk-loading');
    } else {
      box.toggleClass('sk-loading');
        }
    }



    /* SAVE MODAL FORM STORE */
    $(".bs-example-modal-lg").on("submit", ".js-form-store", function () {
      var form = $(this);
      simpleLoad(form, true);
      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          simpleLoad(form, false);
          if (data.form_is_valid) {
            $(".bs-example-modal-lg .modal-content").html(data.html_form);
          }
          else {
            if(data.result){console.log(data.result)}
            $(".bs-example-modal-lg .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    });
    $("#price").on("submit", ".js-form-store", function () {
      var form = $(this);
      simpleLoad($('#price'), true);
      $('.help-block.text-danger').remove();
      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          simpleLoad($('#price'), false);
          if (data.form_is_valid) {
            $(".bs-example-modal-lg").modal("show");
            $(".bs-example-modal-lg .modal-content").html(data.html_form);
          }
          else {
            if(data.result){console.log(data.result)}
            $(".bs-example-modal-lg .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    });
    /* SAVE FORM STORE */
    let basic_button_m = document.querySelector("#basic-plan-btn-m");
    let basic_button_y = document.querySelector("#basic-plan-btn-y");
    let premium_button_m = document.querySelector("#premium-plan-btn-m");
    let premium_button_y = document.querySelector("#premium-plan-btn-y");
    $('#basic-btn-m').click(function(){
      flag_b_m = true;
      flag_b_y = false;
      flag_e_m = false;
      flag_e_y = false;

    })
    $('#basic-btn-y').click(function(){
      flag_b_m = false;
      flag_b_y = true;
      flag_e_m = false;
      flag_e_y = false;
    })
    $('#premium-btn-m').click(function(){
      flag_b_m = false;
      flag_b_y = false;
      flag_e_m = true;
      flag_e_y = false;
    })
    $('#premium-btn-y').click(function(){
      flag_b_m = false;
      flag_b_y = false;
      flag_e_m = false;
      flag_e_y = true;
    })
        // Create a Checkout Session with the selected plan ID
    var createCheckoutSession = function(priceId,) {
      return fetch("/panel/create-checkout-session/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          priceId: priceId,
          email: $('#id_email').val(),
          store: $('#id_name').val(),
          first_name: $('#id_first_name').val(),
          last_name: $('#id_last_name').val(),
          pass: $('#pass').val(),
        })
      }).then(handleFetchResult);

    };
    $('#price').prepend("<div class='sk-spinner sk-spinner-three-bounce'><div class='sk-bounce1'></div><div class='sk-bounce2'></div><div class='sk-bounce3'></div></div>");
    
    /*
    // $(".form-store").on("submit", ".js-form-store", function () {
    //   var form = $(this);
    //   simpleLoad($('#price'), true);
    //   $.ajax({
    //     url: form.attr("action"),
    //     data: form.serialize(),
    //     type: form.attr("method"),
    //     dataType: 'json',
    //     success: function (data) {
    //       if (data.form_is_valid) {
    //         $("#span-1").html("");
    //         $("#span-2").html("");
    //         flag = true;
    //         /* Get your Stripe publishable key to initialize Stripe.js */
    //         fetch("/panel/config/")
    //         .then(handleFetchResult)
    //         .then(function(json) {
    //             var publicKey = json.publicKey;
    //             var basicPrice_m = json.basicPrice_m;
    //             var basicPrice_y = json.basicPrice_y;
    //             var premiumPrice_m = json.premiumPrice_m;
    //             var premiumPrice_y = json.premiumPrice_y;
    //             var stripe = Stripe(publicKey);
    //             // Setup event handler to create a Checkout Session when button(BasicMonth) is clicked
    //             if(basic_button_m !== null && flag_b_m == true) {
    //                 createCheckoutSession(basicPrice_m).then(function(data) {
    //                   // Call Stripe.js method to redirect to the new Checkout page
    //                     simpleLoad($('#price'), false);
    //                     stripe
    //                     .redirectToCheckout({
    //                       sessionId: data.sessionId
    //                     })
    //                     .then(handleResult);

    //                 });
    //             }


    //             // Setup event handler to create a Checkout Session when button(BasicYear) is clicked
    //             if(basic_button_y !== null && flag_b_y == true){
    //                 createCheckoutSession(basicPrice_y).then(function(data) {
    //                   // Call Stripe.js method to redirect to the new Checkout page
    //                     simpleLoad($('#price'), false);
    //                     stripe
    //                     .redirectToCheckout({
    //                       sessionId: data.sessionId
    //                     })
    //                     .then(handleResult);
    //                 });
    //             }


    //             // Setup event handler to create a Checkout Session when button(premiumMonth) is clicked
    //             if(premium_button_m !== null && flag_e_m == true) {
    //                 createCheckoutSession(premiumPrice_m).then(function(data) {
    //                   // Call Stripe.js method to redirect to the new Checkout page
    //                   simpleLoad($('#price'), false);
    //                   stripe
    //                   .redirectToCheckout({
    //                     sessionId: data.sessionId
    //                   })
    //                   .then(handleResult);
    //                 });
    //             }

    //             // Setup event handler to create a Checkout Session when button(premiumYear) is clicked
    //             if(premium_button_y !== null && flag_e_y == true){
    //                 createCheckoutSession(premiumPrice_y).then(function(data) {
    //                   // Call Stripe.js method to redirect to the new Checkout page
    //                   simpleLoad($('#price'), false);
    //                   stripe
    //                   .redirectToCheckout({
    //                     sessionId: data.sessionId
    //                   })
    //                   .then(handleResult);
    //                 });
    //             }
    //           });
    //       }
    //       else {
    //         simpleLoad($('#price'), false);
    //         $("#span-1").html("");
    //         $("#span-2").html("");
    //         flag = false;
    //         $.each(data.user, function(idx, value) {
    //           console.log(value, idx);
    //           $("#id_" + idx).parent().addClass('form-control.error');
    //           // $("#id_" + idx).addClass('errormsg');
    //           $("#id_" + idx).after("<span id='span-1' class='help-block text-danger'>" + value + "</span>");
    //           })
    //         $.each(data.store_form, function(idx, value) {
    //           console.log(value, idx);
    //           $("#id_" + idx).parent().addClass('form-control.error');
    //           // $("#id_" + idx).addClass('errormsg');
    //           $("#id_" + idx).after("<span  id='span-2' class='help-block text-danger'>" + value + "</span>");
    //         })
    //       }
    //     }
    //   });
    //   return false;
    // });*/
    $('#footer').on('submit', '.js-form-contact', function(){
      var form = $(this);
      console.log(form)
      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            $("#contact-text").append("<h4 class='titlebottom'>Correo enviado <i class='icon-check'></i></h4>");
            form.trigger("reset");
            toastr.success("Su correo ha sido enviado satisfactoriamente");
          }
          else {
            $("#contact-text").append("<h4 class='titlebottom'>Error al enviar <i class='icon-times'></i></h4>");
          }
        }
      });
      return false;
      });

// If a fetch error occurs, log it to the console and show it in the UI.
var handleFetchResult = function(result) {
  if (!result.ok) {
    return result.json().then(function(json) {
      if (json.error && json.error.message) {
        throw new Error(result.url + ' ' + result.status + ' ' + json.error.message);
      }
    }).catch(function(err) {
      showErrorMessage(err);
      throw err;
    });
  }
  return result.json();
};



// Handle any errors returned from Checkout
var handleResult = function(result) {
  if (result.error) {
    showErrorMessage(result.error.message);
  }
};

var showErrorMessage = function(message) {
  var errorEl = document.getElementById("error-message")
  errorEl.textContent = message;
  errorEl.style.display = "block";
};

});
