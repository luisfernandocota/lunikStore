$(document).ready(function(){
    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get("session_id")
    function simpleLoad(box, state) {
        if (state) {
            box.toggleClass('sk-loading');
        } else {
            box.toggleClass('sk-loading');
            }
        }
    var box = $('#congrats')
    $('#congrats').prepend("<div class='sk-spinner sk-spinner-three-bounce'><div class='sk-bounce1'></div><div class='sk-bounce2'></div><div class='sk-bounce3'></div></div>");
    simpleLoad(box, true)
    if (sessionId) {
        fetch('/inicio/payment-success/?session_id='+ sessionId, {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
                sessionId: sessionId
              })
        })
        .then((result) => { return result.json();})
        .then((data) => {
            if (data.session){
                simpleLoad(box, false)
                $('#subtitle').text('Tienda creada');
                $('#success').text('¡TU TIENDA HA SIDO CREADA!');
                $('#info1').text('Te hemos enviado un email al correo')
                $('#email').text(data.session['customer_email']);
                $('#info2').text('para que finalices el proceso de activación de tu cuenta.');
                $('#btn-store').text('¡EMPIEZA A VENDER!');
                $('#btn-store').attr('href', 'https://'+data.session['metadata']['store']+'.4shop.mx/panel/');
            }
            if(data.res){
                simpleLoad(box, false)
                $('#subtitle').text('Error');
                $('#success').text('¡UPS, HUBO UN PROBLEMA!');
                $('#info1').text('Te sugerimos volverlo a intentar. No se te ha hecho ningun cobro.')
                $('#btn-store').text('Reintentarlo');
                $('#btn-store').attr('href', 'https://4shop.mx/inicio/planes/');
            }
        })
    }
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
})