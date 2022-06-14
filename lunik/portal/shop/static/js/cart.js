
function radioCheck(method){
    if(document.getElementById("default").checked){
        document.getElementById("p-default").style = "font-size:20px;";
        document.getElementById("p-local").style = "font-size:14px;";
        document.getElementById("p-nacional").style = "font-size:14px;";

    } else if(document.getElementById("local").checked){
        document.getElementById("p-default").style = "font-size:14px;";
        document.getElementById("p-local").style = "font-size:20px;";
        document.getElementById("p-nacional").style = "font-size:14px;";


    } else if(document.getElementById("nacional").checked){
        document.getElementById("p-default").style = "font-size:14px;";
        document.getElementById("p-local").style = "font-size:14px;";
        document.getElementById("p-nacional").style = "font-size:20px;";

    } 
    shippingMethod(method)

}
function simpleLoad(box, state) {
    if (state) {
        box.toggleClass('sk-loading');
    } else {
        box.toggleClass('sk-loading');
        }
    }
function shippingMethod(method){
    let params = new URLSearchParams(window.location.search);
    let url = '/carrito/checkout/?step='+params.get('step')
    $.ajax({
    url: url,
    data: {'method':method},
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
        simpleLoad($('.dynamic-detail'), true);
        $('.dynamic-detail').prepend('<div class=loader text-center"><span class="bar"></span><span class="bar"></span><span class="bar"></span> </div>');
    },
    success: function (data) {
            history.pushState({}, null, window.location.origin + '/carrito/checkout/?step='+data.step+'&method='+data.method);
            simpleLoad($('.dynamic-detail'), false);
            $(".dynamic-step").html(data.html_dynamic);
            $(".dynamic-footer").html(data.html_footer);
            $(".dynamic-detail").html(data.html_dynamic_detail);
            $(".dynamic-breadcrumb").html(data.html_dynamic_breadcrumb);

            $('#'+data.method).prop("checked", true);
            $('#p'+data.method).css("font-size", "20px");

            $('#span-method').val(data.method)
        }
    });
}
    