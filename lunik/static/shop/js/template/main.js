$(document).ready(function () {

    const principal_carousel = $(".principal-carousel");
    principal_carousel.owlCarousel({
      margin: 0,
      nav: false,
      dots: true,
      loop: true,
      items: 1,
      smartSpeed:450
    });
    const brands = $(".brands-carousel");
    brands.owlCarousel({
      margin: 0,
      nav: false,
      dots: true,
      loop: true,
      items: 6,
      smartSpeed:450,
      responsive:{
          0:{
            items:1,
            nav:false
          },
          992:{
              items:6
          }
      }
    });
    const login = $(".carousel-clean-one");
    login.owlCarousel({
      margin: 1,
      nav: false,
      dots: false,
      loop: true,
      items: 1,
      autoplay:true,
      autoplayTimeout:5000,
      autoplayHoverPause:true,
      smartSpeed:800
    });
    const top_products = $(".top-products-carousel");
    top_products.owlCarousel({
      margin: 0,
      nav: true,
      loop: true,
      items: 3,
      smartSpeed:450
    });
    
    var margin_top_mega_menu = $('#principal-menu-container').height() + $('#promotions-ribbon').height() + 30;    
    $("#mega-menu").css('margin-top', margin_top_mega_menu)

    $(".mega-menu").css('display', 'none')
    console.log($('#id_quantity'));
});


/** Increment or decrement input quanity product detail */
var input_quantity_int = parseInt($('#id_quantity').val());
var input_quantity = $('#id_quantity');
$('.cart-table').on('click', '.button-add', function (e) {
  try {
      if(input_quantity_int < 99){
        input_quantity_int++;
        $('#id_quantity').val(input_quantity_int);
      }
  } catch (e){
    console.log(e);
  }
}).trigger('change');
$('.cart-table').on('click', '.button-rest', function (e) {
  try {
      if(input_quantity_int > 1){
        input_quantity_int -= 1;
        $('#id_quantity').val(input_quantity_int);
      }
  } catch (e){
    console.log(e);
  }
}).trigger('change');


/** Elements */
let mega_menu_trigger = document.getElementsByClassName("mega-menu-trigger")[0];
let mega_menu = document.getElementsByClassName("mega-menu")[0];

try {
  
  mega_menu_trigger.addEventListener(
    "click",
    function (event) {
        $(".mega-menu").css('display', 'block')
        setTimeout(function(){
          $(".mega-menu").addClass("on");
        },50)
    },
    false
  );
  
  mega_menu.addEventListener(
    "mouseover",
    function (event) {
      $(".mega-menu").css('display', 'block')
      setTimeout(function(){
        $(".mega-menu").addClass("on");
      },50)
    },
    false
  );
  
  mega_menu.addEventListener(
    "mouseleave",
    function (event) {
      $(".mega-menu").removeClass("on");
      setTimeout(function(){
        $(".mega-menu").css('display', 'none')
      },500)
    },
    false
  );

} catch (error) {
  console.log(error)
  console.log("No hay menu.")
}





$('.mini-product-preview').on('click', function(event) {
  event.preventDefault();
  $('.img-zoom-lens').remove()
  let selectPhoto = event.currentTarget.attributes['imgTo'].value
  $('.product-preview').removeClass('show')
  $(`.${selectPhoto}`).addClass('show')
  imageZoom(selectPhoto, "zoom");
})


$('.cartBarToggle').on('click', function(event) {
  event.preventDefault();
  $('.cart-bar').toggleClass('toggled');
})
$('.menuBarToggle').on('click', function(event) {
  event.preventDefault();
  $('.mobile-menu').toggleClass('toggled');
})
$('.panelToggle').on('click', function(event) {
  event.preventDefault();
  $('.panel-menu').toggleClass('toggled');
})
$('.menuUserMobileToggle').on('click', function(event) {
  event.preventDefault();
  $('.mobile-user-menu').toggleClass('toggled');
})

function showCategory(category, checkbox)
{
  if(category==='all')
  {
    $('.article-result').removeClass('show');
    $('.article-result').addClass('show')
  }
  else{
    $('.article-result').removeClass('show');
    setTimeout(function(){
      $(`.${category}`).addClass('show');
    }, 100)
  }
}



window.onscroll = function() {
  if(window.scrollY > 80)
  {
    if(!$('#principal-menu-container').hasClass("on"))
    {
      $('#principal-menu-container').addClass('on')
      $('#mega-menu').addClass('resolve-top')
      margin_top_mega_menu = $('#principal-menu-container').height();    
      $("#mega-menu").css('margin-top', margin_top_mega_menu)
    }
  }
  else{
    $('#principal-menu-container').removeClass('on')
    $('#mega-menu').removeClass('resolve-top')
    margin_top_mega_menu = $('#principal-menu-container').height() + $('#promotions-ribbon').height() + 30;    
      $("#mega-menu").css('margin-top', margin_top_mega_menu)
  }
};
