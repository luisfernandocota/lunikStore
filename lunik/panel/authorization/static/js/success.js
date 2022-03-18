const urlParams = new URLSearchParams(window.location.search);
const sessionId = urlParams.get("session_id")
let customerId;

function simpleLoad(box, state) {
    if (state) {
      box.toggleClass('sk-loading');
    } else {
      box.toggleClass('sk-loading');
        }
    }
    simpleLoad($('.ibox-content'), true)
if (sessionId) {
  fetch("/panel/get-checkout-session/", {
        method: "POST",
        headers: {
        "Content-Type": "application/json"
        },
        body: JSON.stringify({
        sessionId: sessionId,
        })
    })
    .then(function(result){
      return result.json()
    })
    .then(function(session){
        simpleLoad($('.ibox-content'), false)
      // We store the customer ID here so that we can pass to the
      // server and redirect to customer portal. Note that, in practice
      // this ID should be stored in your database when you receive
      // the checkout.session.completed event. This demo does not have
      // a database, so this is the workaround. This is *not* secure.
      // You should use the Stripe Customer ID from the authenticated
      // user on the server.
      console.log(session)
      amount_total = parseInt(session.amount_total/100).toFixed(2)
      $('#amount').text('$'+amount_total+' '+session.currency.toUpperCase())
      customerId = session.customer;

    })
    .catch(function(err){
      console.log('Error when fetching Checkout session', err);
    })

  // In production, this should check CSRF, and not pass the session ID.
  // The customer ID for the portal should be pulled from the 
  // authenticated user on the server.
}