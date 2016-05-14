appJsUrl = 'http://wolverine.ccom.uprrp.edu/~jdelacruz/netFlows/apiJS/Style/js/app.js';
userDefineUrl = 'http://wolverine.ccom.uprrp.edu/~jdelacruz/netFlows/apiJS/Style/js/userDefine.js';
cssUrl = 'http://wolverine.ccom.uprrp.edu/~jdelacruz/netFlows/apiJS/Style/css/main.css'
engineUrl = 'http://wolverine.ccom.uprrp.edu/~jdelacruz/netFlows/apiJS/engine.cgi';

function setUrls(){
	var head = document.getElementsByTagName('head')[0];

	var appScript = document.createElement('script');
	var userDefScript = document.createElement('script');
	var cssLink = document.createElement('link');

	appScript.src = appJsUrl;
	head.appendChild(appScript);

	userDefScript.src = userDefineUrl;
	head.appendChild(userDefScript);

	cssLink.rel = "stylesheet";
	cssLink.type = "text/css";
	cssLink.href = cssUrl;
	head.appendChild(cssLink)
}

setUrls();