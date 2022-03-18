// STRIPE CONFS URLS
$(document).ready(function() {
  function simpleLoad(box, state) {
    if (state) {
      box.toggleClass('sk-loading');
    } else {
      box.toggleClass('sk-loading');
        }
    }
    let basic_button_m = document.querySelector("#basic-plan-btn-m");
    let basic_button_y = document.querySelector("#basic-plan-btn-y");
    let premium_button_m = document.querySelector("#premium-plan-btn-m");
    let premium_button_y = document.querySelector("#premium-plan-btn-y");

        // Create a Checkout Session with the selected plan ID
    var createCheckoutSession = function(priceId,) {
      return fetch("/panel/create-checkout-session/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          priceId: priceId,
        })
      }).then(handleFetchResult);

    };
    
    fetch("/panel/config/")
    .then(handleFetchResult)
    .then(function(response){ return response.json();})
    .then(function(json) {
        var publicKey = json.publicKey;
        var basicPrice_m = json.basicPrice_m;
        var basicPrice_y = json.basicPrice_y;
        var premiumPrice_m = json.premiumPrice_m;
        var premiumPrice_y = json.premiumPrice_y;
        var stripe = Stripe(publicKey);
        // Setup event handler to create a Checkout Session when button(BasicMonth) is clicked
        if(basic_button_m !== null) {
          basic_button_m.addEventListener("click", () => {
            createCheckoutSession(basicPrice_m).then(function(data) {
              // Call Stripe.js method to redirect to the new Checkout page
                simpleLoad($('#price'), false);
                stripe
                .redirectToCheckout({
                  sessionId: data.sessionId
                })
                .then(handleResult);

            });
          })
        }


        // Setup event handler to create a Checkout Session when button(BasicYear) is clicked
        if(basic_button_y !== null){
          basic_button_y.addEventListener("click", () => {
            createCheckoutSession(basicPrice_y).then(function(data) {
              // Call Stripe.js method to redirect to the new Checkout page
                simpleLoad($('#price'), false);
                stripe
                .redirectToCheckout({
                  sessionId: data.sessionId
                })
                .then(handleResult);
            });
          })
        }


        // Setup event handler to create a Checkout Session when button(premiumMonth) is clicked
        if(premium_button_m !== null) {
          premium_button_m.addEventListener("click", () => {
            createCheckoutSession(premiumPrice_m).then(function(data) {
              // Call Stripe.js method to redirect to the new Checkout page
              simpleLoad($('#price'), false);
              stripe
              .redirectToCheckout({
                sessionId: data.sessionId
              })
              .then(handleResult);
            });
          })
        }

        // Setup event handler to create a Checkout Session when button(premiumYear) is clicked
        if(premium_button_y !== null){
          premium_button_y.addEventListener("click", () => {
            createCheckoutSession(premiumPrice_y).then(function(data) {
              // Call Stripe.js method to redirect to the new Checkout page
              simpleLoad($('#price'), false);
              stripe
              .redirectToCheckout({
                sessionId: data.sessionId
              })
              .then(handleResult);
            });
          })
        }
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