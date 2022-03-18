// Create a Checkout Session with the selected plan ID
var createCheckoutSession = function (priceId) {
  return fetch('/create-checkout-session', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      priceId: priceId,
    }),
  }).then(function (result) {
    return result.json();
  });
};

// Handle any errors returned from Checkout
var handleResult = function (result) {
  if (result.error) {
    var displayError = document.getElementById('error-message');
    displayError.textContent = result.error.message;
  }
};

/* Get your Stripe publishable key to initialize Stripe.js */
fetch('/setup')
  .then(function (result) {
    return result.json();
  })
  .then(function (json) {
    var publishableKey = 'pk_test_51H5LaSIKF8Hi9Jx6Uetqcf1TSvBOFZBVTe69PKuV9Xir5fkMwC3O4bifcGS5cV41jDxQfdMJiTgjhAj5g0Mtf2Lo00WmU2jh8X';
    var basicPriceId = json.basicPrice;
    var proPriceId = json.proPrice;

    var stripe = Stripe(publishableKey);
    // Setup event handler to create a Checkout Session when button is clicked
    document
      .getElementById('basic-plan-btn')
      .addEventListener('click', function (evt) {
        document.querySelectorAll('button').forEach((bt) => {
          bt.disabled = true;
        });
        createCheckoutSession(basicPriceId).then(function (data) {
          // Call Stripe.js method to redirect to the new Checkout page
          stripe
            .redirectToCheckout({
              sessionId: data.sessionId,
            })
            .then(handleResult);
        });
      });

    // Setup event handler to create a Checkout Session when button is clicked
    document
      .getElementById('pro-plan-btn')
      .addEventListener('click', function (evt) {
        document.querySelectorAll('button').forEach((bt) => {
          bt.disabled = true;
        });
        createCheckoutSession(proPriceId).then(function (data) {
          // Call Stripe.js method to redirect to the new Checkout page
          stripe
            .redirectToCheckout({
              sessionId: data.sessionId,
            })
            .then(handleResult);
        });
      });
  });