document.documentElement.className="js";var tal=function(){function e(e,t){var n=e.split(".").pop(),a="js"==n,r=document.createElement(a?"script":"link");r.onload=r.onreadystatechange=function(){r.readyState&&"loaded"!=r.readyState&&"complete"!=r.readyState||("string"==typeof t&&o.push(t),r.onload=r.onreadystatechange=null)},a?(r.type="text/javascript",r.src=e):(r.rel="stylesheet",r.href=e),document.getElementsByTagName("head")[0].appendChild(r)}function t(t,o,r){if("string"==typeof o){if(a.indexOf(o)>=0)return;a.push(o)}"undefined"==typeof r?e(t,o):n(r,function(){e(t,o)})}function n(e,t){var a="string"==typeof e?[e]:e;for(var r in a)if(o.indexOf(a[r])<0)return void setTimeout(function(){n(a,t)},99);setTimeout(t,99)}var a=[],o=[];return{ready:n,load:t}}();