appJsUrl = 'http://wolverine.ccom.uprrp.edu/~jdelacruz/netFlows/api/Style/js/app.js';
cssUrl = 'http://wolverine.ccom.uprrp.edu/~jdelacruz/netFlows/api/Style/css/main.css'
engineUrl = 'http://wolverine.ccom.uprrp.edu/~jdelacruz/netFlows/api/engine.cgi';

function setUrls(){
	var head = document.getElementsByTagName('head')[0];

	var appScript = document.createElement('script');
	var cssLink = document.createElement('link');

	appScript.src = appJsUrl;
	head.appendChild(appScript);

	cssLink.rel = "stylesheet";
	cssLink.type = "text/css";
	cssLink.href = cssUrl;
	head.appendChild(cssLink)
}

setUrls();