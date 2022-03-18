//This is your test publishable API key.
const stripe = Stripe("pk_test_51H5LaSIKF8Hi9Jx6Uetqcf1TSvBOFZBVTe69PKuV9Xir5fkMwC3O4bifcGS5cV41jDxQfdMJiTgjhAj5g0Mtf2Lo00WmU2jh8X");
checkStatus();

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

    $.ajax({
        url: '/carrito/checkout/retrievePayment/',
        data: JSON.stringify({ paymentIntent }),
        type: 'POST',
        dataType: 'json',
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
        success: function (data) {
            if(data.exists){
              return window.location = data.url_redirect
            } else {
              $("#section-payment").html(data.html_succeeded);
            }
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