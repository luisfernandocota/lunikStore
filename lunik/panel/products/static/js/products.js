$(document).ready(function(){


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
    function simpleLoad(box, state) {
        if (state) {
            box.toggleClass('sk-loading');
        } else {
            box.toggleClass('sk-loading');
            }
        }
    $(".card-header").on("submit", ".js-search-form", function () {
        var form = $(this);
        $.ajax({
          url: form.attr("action"),
          data: form.serialize(),
          type: form.attr("method"),
          dataType: 'json',
          beforeSend: function(){
            simpleLoad($('#box-content'), true);
            $('#box-content').prepend("<div class='sk-spinner sk-spinner-three-bounce'><div class='sk-bounce1'></div><div class='sk-bounce2'></div><div class='sk-bounce3'></div></div>");
          },
          success: function (data) {
            simpleLoad($('#box-content'), false);
            if (data.search_valid) {
              $(".card-products").empty();
              $(".card-products").append(data.html_orders);
              feather.replace();
    
            }else{
              toastr.error(data.message);
            }
          }
        });
        return false;
    });
})