//This is your test publishable API key.
const stripe = Stripe($('#stripe_public_key').val());
checkStatus();
function simpleLoad(box, state) {
  if (state) {
      box.toggleClass('sk-loading');
  } else {
      box.toggleClass('sk-loading');
      }
  }
async function checkStatus() {
 const clientSecret = new URLSearchParams(window.location.search).get(
   "payment_intent_client_secret"
 );

 if (!clientSecret) {
   return;
 }

 const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);
 let csrftoken = $('input[name="csrfmiddlewaretoken"]').attr('value');
 switch (paymentIntent.status) {
   case "succeeded":
    simpleLoad($('.payment-section'), true);

    $.ajax({
        url: '/carrito/checkout/retrievePayment/',
        data: JSON.stringify({ paymentIntent }),
        type: 'POST',
        dataType: 'json',
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
        success: function (data) {
            $("#section-payment").html(data.html_succeeded);
            simpleLoad($('.payment-section'), false);
            $('#pk-loader').remove();
        }
      });
     // showMessage("Payment succeeded!");
     break;
   case "processing":
     // showMessage("Your payment is processing.");
     break;
   case "requires_payment_method":
     // showMessage("Your payment was not successful, please try again.");
     break;
   default:
     // showMessage("Something went wrong.");
     break;
 }
}