/**
 * Created by nennogabriel on 4/21/16.
 *
 * Change to TAL project
 */

var charm = {
	q: [], // queue
	r: [], // ready to use.
	lib: {},
	ready: function(list, callback){
		if(typeof(list) == "string"){list = [list]}
		var ready = true, i;
		for(i in list){
			if(charm.r.indexOf(list[i]) < 0){
				charm.l(list[i]);
				ready = false;
			}
		}
		if(ready){
			callback();
		} else {
			setTimeout(function(){
				charm.ready(list, callback)
			}, 99);
		}

	},
	l: function(ref){ // Load files asyncronisly
		var url = charm.lib[ref],
			ext = url.split(".").pop(),
			js = ext == "js",
			el = document.createElement((js ? 'script': 'link'));
		el.onload = el.onreadystatechange = function(){
			if(!el.readyState || el.readyState == 'loaded' || el.readyState == 'complete') {
				charm.r.push(ref);
				charm.q.pop(ref);
				el.onload = el.onreadystatechange = null;
			}
		};
		if(js){
			// el.type = "text/javascript";
			el.async = true;
			el.src = url;
		} else{
			el.rel = "stylesheet";
			el.href = url;
		}
		document.getElementsByTagName('head')[0].appendChild(el);
	}
};