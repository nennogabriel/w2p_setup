// // loading images
//
// $("img[data-src]").attr("src", function(){
//     var w = $(this).width(),
//         h = $(this).height(),
//         parts = $(this).data("src").split(".");
//     var size = Math.max(w,h) * window.devicePixelRatio;
//     parts.splice(1,0, size);
//     var src = $(this).attr("src");
//     $(this).data("src", src);
//     $(this).removeAttr("data-src");
//     return parts.join(".");
// });

// function optimalSizeToDevice(original){
//   var ratio = window.devicePixelRatio,
//       width = original[0] * Math.sqrt(ratio),
//       height = original[1] * Math.sqrt(ratio);
//   return [width, height]
// }

function getOptimalSizeName(el, source){
    var parts = source.split("."),
        r = window.devicePixelRatio,
        w = el.width,
        h = el.height;
    if (parts.length == 2) {
        w = Math.ceil(w * Math.sqrt(r));
        h = Math.ceil(h * Math.sqrt(r));
        var size = w + "x" + h;
        parts.splice(1,0,size);
    } else {
        var x = "x",
            midle = parts[1];
        if (midle === "device") {
            w = $(window).width();
            h = $(window).height();
        } else if (midle === "max" || midle === "min") {
            (midle === "max" ? x = Math.max(w, h) : x = Math.min(w, h));
            w = "";
            h = "";
        } else {
            x = midle;
            w = "";
            h = "";
        }
        if (w) {w = Math.ceil(w * Math.sqrt(r));}
        if (h) {h = Math.ceil(h * Math.sqrt(r));}
        parts[1] = w + x + h;
    }
    return parts.join(".");
}


/**
 * jQuery Unveil
 * A very lightweight jQuery plugin to lazy load images
 * http://luis-almeida.github.com/unveil
 *
 * Licensed under the MIT license.
 * Copyright 2013 Luís Almeida
 * https://github.com/luis-almeida
 */

;(function($) {

  $.fn.unveil = function(threshold, callback) {

    var $w = $(window),
        th = threshold || 0,
        // retina = window.devicePixelRatio > 1,
        // attrib = retina? "data-src-retina" : "data-src",
        images = this,
        loaded;

    this.one("unveil", function() {
      // var source = this.getAttribute(attrib);
      var source = this.getAttribute("data-src");
      if (source) {
        if (source[0] == "/" && source[1] != "/"){source = getOptimalSizeName(this, source)};
        this.setAttribute("src", source);
        this.removeAttribute("data-src");
        if (typeof callback === "function") callback.call(this);
      }
    });

    function unveil() {
      var inview = images.filter(function() {
        var $e = $(this);
        if ($e.is(":hidden")) return;

        var wt = $w.scrollTop(),
            wb = wt + $w.height(),
            et = $e.offset().top,
            eb = et + $e.height();

        return eb >= wt - th && et <= wb + th;
      });

      loaded = inview.trigger("unveil");
      images = images.not(loaded);
    }

    $w.on("scroll.unveil resize.unveil lookup.unveil", unveil);

    unveil();

    return this;

  };

})(window.jQuery);