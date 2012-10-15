function getElementsByClass( searchClass, domNode, tagName) { 
	if (domNode == null) domNode = document;
	if (tagName == null) tagName = '*';
	var el = new Array();
	var tags = domNode.getElementsByTagName(tagName);
	var tcl = " "+searchClass+" ";
	for(i=0,j=0; i<tags.length; i++) { 
		var test = " " + tags[i].className + " ";
		if (test.indexOf(tcl) != -1) 
			el[j++] = tags[i];
	} 
	return el;
} 
// sharing functions
function socialNetworkShare(type, pageLoc, url, msg, imgURL){
	var url = url||location.href;
	var joiner = "?";
	if(url.indexOf("?") != -1) joiner = "&"; 
	var msg_original = msg||document.title;
	var msg = encodeURIComponent(msg||document.title);
	var pageLoc = encodeURIComponent(pageLoc||'');
	var pathPrefix, pathShare;
	
	switch(type){
		case "facebook":
			url = encodeURIComponent(url+joiner+"utm_source=facebook&utm_medium=social_media&utm_content=pdp_share");
			pathPrefix = "http://www.facebook.com/sharer.php?";
			pathShare = pathPrefix + "u=" + url + "&t=" + msg;
			_gaq.push(
				['_trackSocial', 'Facebook', 'Share', msg_original, pathShare]
			);
			break;
		case "twitter":
			url = encodeURIComponent(url+joiner+"utm_source=twitter&utm_medium=social_media&utm_content=pdp_share");
			pathPrefix = "http://twitter.com/share?";
			pathShare = pathPrefix + "url=" + url + "&text=" + msg;
			_gaq.push(
				['_trackSocial', 'Twitter', 'Share', msg_original, pathShare]
			);
			break;
		case "weibo":
			url = encodeURIComponent(url+joiner+"utm_source=weibo&utm_medium=social_media&utm_content=pdp_share");
			pathPrefix = "http://service.t.sina.com.cn/share/share.php?";
			pathShare = pathPrefix + "url=" + url + "&title=" + msg;
			_gaq.push(
				['_trackSocial', 'Weibo', 'Share', msg_original, pathShare]
			);
			break;
		case "renren":
			url = encodeURIComponent(url+joiner+"utm_source=renren&utm_medium=social_media&utm_content=pdp_share");
			pathPrefix = "http://share.renren.com/share/buttonshare.do?";
			pathShare = pathPrefix + "link=" + url + "&title=" + msg;
			_gaq.push(
				['_trackSocial', 'RenRen', 'Share', msg_original, pathShare]
			);
			break;
		case "pinit":
			url = encodeURIComponent(url+joiner+"utm_source=pinterest&utm_medium=social_media&utm_content=pdp_share");
			pathPrefix = "http://pinterest.com/pin/create/button/?";
			var currentImg = $("#HeroImagePlane img.l").eq($("#HeroImagePlane").data("imgIdx")).attr("src");
			pathShare = pathPrefix + "url=" + url + "&media=" + currentImg + "&description=" + msg;
			_gaq.push(
				['_trackSocial', 'Pinterest', 'Share', msg_original]
			);
			break;
		case "pinterest":
			url = encodeURIComponent(url+joiner+"utm_source=pinterest&utm_medium=social_media&utm_content=pdp_share");
			pathPrefix = "http://pinterest.com/pin/create/button/?";
			var allProductImgs = getElementsByClass('fancybox-thumb',null,'A');
			if(allProductImgs.length > 0){
				// console.log(allProductImgs[0]);
				for(var i=0; i < allProductImgs.length; i++){
					if(allProductImgs[i].style.display !== 'none'){
						// console.log(allProductImgs[i].style.display);
						// console.log(allProductImgs[i].getElementsByTagName('img')[0].src);
						imgURL = allProductImgs[i].getElementsByTagName('img')[0].src;
						// console.log(allProductImgs[i].childNodes[0].attr("src"));
						break;
					}
				}
			}
			var currentImg = imgURL;
			pathShare = pathPrefix + "url=" + url + "&media=" + currentImg + "&description=" + msg;
			_gaq.push(
				['_trackSocial', 'Pinterest', 'Share', msg_original]
			);
			break;
		
	}
	
	window.open(pathShare,"_blank","toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width=640, height=480");
	return false;
}
