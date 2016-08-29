var wfiEvent = (function () {
  var timers = {};
  return function (callback, ms, uniqueId) {
    // if (!uniqueId) {
    //   uniqueId = "Don't call this twice without a uniqueId";
    // }
    if (timers[uniqueId]) {
      clearTimeout (timers[uniqueId]); 
    }
    timers[uniqueId] = setTimeout(callback, ms);
  };
})();



// tal.load("https://cdnjs.cloudflare.com/ajax/libs/node-waves/0.7.5/waves.min.css", "waves.css");
// tal.load("https://cdnjs.cloudflare.com/ajax/libs/node-waves/0.7.5/waves.min.js", "waves");
//
// tal.ready(["waves", "jquery"], function () {
//     var config = {
//         duration: 750, // How long Waves effect duration
//         delay: 0 // Delay showing Waves effect on touch (0 to disable delay) (in milliseconds)
//     };
//
//     // Initialise Waves with the config
//     Waves.init(config);
//     Waves.attach('a.btn, button.btn, .btn-large, .nav a.button-collapse', 'waves-light');
//     Waves.attach('.side-nav a', null);
// });

$('a.btn, button.btn, .btn-large, .nav a.button-collapse').addClass('waves-effect waves-light');

$("body").velocity({opacity: 1, animation: 'none'}, {duration: 500});

//=require web2py/web2py.js
$('.w2p-toolbar-hidden').hide();
//=require load/images.js

$(document).ready(function(){
    $("img[data-src]").unveil(100);

    // $(".button-collapse.main").sideNav({menuWidth: 256, closeOnClick: true});
    $(".button-collapse.main")
        .click(function(){$(".button-collapse.more").sideNav('hide');})
        .sideNav({menuWidth: 264});
    // $(".button-collapse.more").sideNav({edge: 'right', menuWidth: 256, closeOnClick: true});
    $(".button-collapse.more")
        .click(function(){$(".button-collapse.main").sideNav('hide')})
        .sideNav({edge: 'right', menuWidth: 264, closeOnClick: true});
    $(".dropdown-button").dropdown();
    $(".collapsible").collapsible();
    $('.tooltipped').tooltip({delay: 50});
    $('.parallax').parallax();
    $('.modal-trigger, a[href="#contact_form"]').leanModal();
    $('select').material_select();
    $('input.date').pickadate({
        format: 'yyyy-mm-dd',
        selectMonths: true,
        selectYears: 10
    });

    var text = $('.w2p_flash').text();
    if(text){Materialize.toast(text, 4000);}


    $(function(){
        var lastScrollTop = 0, delta = ($(window).height() * 0.20);
        $(window).scroll(function(event){
            var st = $(this).scrollTop();
            if (st < 192){
                $('html').addClass('scroll-up').removeClass('scroll-down');
            }
            if (st < 1){
                $('html').addClass('scroll-at-top');
            }else{
                $('html').removeClass('scroll-at-top');
            }
            if (Math.abs(lastScrollTop - st) <= delta) {
                wfiEvent(function () {
                    lastScrollTop = st;
                }, 250, 'scroll-control');
                return;
            }
            if (st > lastScrollTop){
               $('html').addClass('scroll-down').removeClass('scroll-up');
            } else {
               $('html').addClass('scroll-up').removeClass('scroll-down');
            }
            lastScrollTop = st;
        });
    });

});

