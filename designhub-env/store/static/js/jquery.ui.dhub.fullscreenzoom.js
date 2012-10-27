var pageY = 0;
var $outer_container = null;
var $imagePan_panning = null;
var $imagePan = null;
var $imagePan_container = null;
var $zoomPan = null;
var $zoomImage = null;
var currentImageHeight = null;
var containerWidth = 0;
var containerHeight = 0;
var totalContentW = 0;
var totalContentH = 0;
var panningOpen = false;
var isMobile = navigator.userAgent.toLowerCase().match(/(iphone|ipod|ipad|android)/i);
var isiPhoneOnly = navigator.userAgent.toLowerCase().match(/(iphone)/i);
var currentFSImg = 1;

function changeME($enlargeEle) {
	currentFSImg = parseInt($enlargeEle.attr('data-index'));
	var superImageUrl = $enlargeEle.attr('data-bigimage-src');
    var imageRatio = $enlargeEle.height() / $enlargeEle.width();
    if (isMobile) {
        document.getElementById("super").src = superImageUrl;
        $("body,html").css("overflow", "hidden");
        $('#outer_container').bind("click", function(e) {
            e.preventDefault();
            closeME();
            return false;
        });
        $("#super").unbind('load');
        $("#super").removeAttr('onload');
        $("#super").attr('onload', function() {
            var auxX = $(this).width();
            var auxY = $(this).height();
            if (navigator.userAgent.toLowerCase().match(/ipad/)) {
                // iPad resolution is bigger than 1000px
                $('#outer_container, body, html, #super').css({ "width": 1280, "height": 1280 * imageRatio });
            } else {
                $('#outer_container, body, html').css({ "width": 1000, "height": 1000 * imageRatio });
            }
            $('#outer_container').show();
            if (!isiPhoneOnly) {
            	$(".prevNextBarContainer").show();
                // $('#dvtPrevNextControls').show();
            }
        });
    } else {
    	document.getElementById("super").src = superImageUrl;
    	
        // var objImg = document.getElementById("views");
        // var src1000 = objImg.src.replace("_400.", "_1000.");
        // if (src1000 != $("#super").attr("src")) {
            // document.getElementById("super").src = src1000;
        // } else {
            // scroll(0, 0);
            resizeME();
        // }
        if ($.browser.msie) {
        	alert(superImageUrl);
            var auxObj = new Image();
            auxObj.onload = onImageLoad;
            auxObj.src = superImageUrl;
            $(window).bind("scroll", function(e) {
                e.preventDefault();
                return false;
            });
            $("html,body").css("overflow", "hidden");
        }
        $('body').css("overflow", "hidden");
        scroll(0, 0);
        _resizeME(false);
    }
    panningOpen = true;
}


function resizeME() {
    _resizeME(true);
}

function _resizeME(blnShow) {
    $outer_container = $("#outer_container");
    
    // $imagePan_panning = $("#imagePan").find(".panning");
    // $imagePan = $("#imagePan");
    // $imagePan_container = $("#imagePan").find(".container");
    $zoomPan = $('#zoomPan');
    $zoomImage = $('#super');
    currentImageHeight = $zoomImage.height();
    $outer_container.css("top", 0);
    $outer_container.width(document.body.clientWidth);

    if (blnShow == true) {
        scroll(0, 0);
        $outer_container.show().focus();
        $(".prevNextBarContainer").show();
    }
    // containerWidth = $imagePan.width();
    // containerHeight = $imagePan.height();
    // totalContentW = $imagePan_panning.width();
    // totalContentH = ($imagePan_panning.height() ? $imagePan_panning.height() : totalContentH);
    // $imagePan_container.css("width", totalContentW).css("height", totalContentH);
    // $imagePan_panning.css('width', document.body.clientWidth);
    containerHeight = $outer_container.height();
    $outer_container.css('height', document.body.clientHeight);
    $('#super').css('width', document.body.clientWidth);
    $('#outer_container').one("click", function(e) {
        e.preventDefault();
        closeME();
        return false;
    });
}
function MouseMove(pageY) {
    if ($.browser.msie) {
        var mouseCoordsY = pageY - $(document).scrollTop();
    } else {
        var mouseCoordsY = pageY;
    }
    var mousePercentY = mouseCoordsY / containerHeight;
    
    var diffBodyHeightConteinerHeight = (currentImageHeight - containerHeight);
    // console.log(mousePercentY);
    // console.log(diffBodyHeightConteinerHeight);
    // console.log(mousePercentY);
    // console.log(diffBodyHeightConteinerHeight*mousePercentY);
    var destY = diffBodyHeightConteinerHeight*mousePercentY;
    $zoomPan.css("top", -destY);
    
    // var destY = -(((totalContentH - containerHeight) - containerHeight) * (mousePercentY));
    // $zoomPan.css("top", -pageY);
    // console.log(pageY);
    // var mousePercentY = mouseCoordsY / containerHeight;
    // var destY = -(((totalContentH - containerHeight) - containerHeight) * (mousePercentY));
    // var thePosC = mouseCoordsY - destY;
// 
    // $imagePan_container.css("top", -thePosC);
}

function onImageLoad() {
    if (panningOpen) {
        if (!isMobile) {
            scroll(0, 0);
            resizeME();
        }
    }
}


$('img#super').load(function() {
    if (panningOpen) {
        if (!isMobile) {
            scroll(0, 0);
            resizeME();
        }
    }
});

function closeME() {
    if (panningOpen) {
    	$('a.product-detail-thumnail[href=#' + (currentFSImg - 1) + ']').trigger('click');
        $("#outer_container, .prevNextBarContainer").fadeOut();
        $("#outer_container").fadeOut();
        if ($.browser.msie) {
            $('html').css('overflow', 'auto');
            $('body').css('overflow', 'visible');
        } else {
            $('body').css('overflow', 'visible');
        }
        if (!isMobile) {
            scroll(0, 0);
        }
        if ($.browser.msie) {
		alert('currentFSImg');
		}else{
		console.log('currentFSImg');
		}
        panningOpen = false;
    }
}

$(window).resize(function() {
    // if (panningOpen && $imagePan != undefined) {
    if (panningOpen) {
        // $imagePan_container.css("top", 0);
        resizeME();
    }
});
if (isMobile) {
    // $("#dvtClickFullScreen").show();
    // $("#zoom01").unbind("mouseover");
} else {
    $('body').bind("mousemove", function(e) {
        pageY = e.pageY;
        if (panningOpen && !isMobile) {
            MouseMove(pageY);
        }
    });
    // bindFullscreenTooltip();
}

$("#prevSuperImage").bind("click", function(e) {
    e.preventDefault();
    e.cancelBubble = true;
    if (e.stopPropagation) e.stopPropagation();

    if (currentFSImg > 1) {
        loadFullScreenImage("prev");
    } else if (currentFSImg == 1) {
        loadFullScreenImage("last");
    }
    return false;
});

$("#nextSuperImage").bind("click", function(e) {
    e.preventDefault();
    e.cancelBubble = true;
    if (e.stopPropagation) e.stopPropagation();

    if (currentFSImg < totalThumbnails) {
        loadFullScreenImage("next");
    } else if (currentFSImg == totalThumbnails) {
        loadFullScreenImage("first");
    }
    return false;
});

function loadFullScreenImage(action) {
    var posToLoad = currentFSImg;
    switch(action) {
        case "next":
            posToLoad += 1;
        break;
        case "prev":
            posToLoad -= 1;
        break;    
        case "first":
            posToLoad = 1;
        break;
        case "last":
            posToLoad = totalThumbnails;
        break;
    }
    var $enlargeEle = $('.fancybox-thumb[data-index=' + posToLoad +']');
    // console.log($enlargeEle.attr('data-index'));
        if ($.browser.msie) {
		}else{
		    console.log(totalThumbnails);
		    console.log(posToLoad);
		}

    changeME($enlargeEle);
    
    // var imgObj = $("#itemThumb" + posToLoad);
    // if (imgObj.length) {
        // imgObj.trigger("click");
        // $("#zoom01").trigger("click");
    // }
}

$('img#super').load(function() {
    if (panningOpen) {
        if (!isMobile) {
            scroll(0, 0);
            resizeME();
        }
    }
});


$('.slides_control .fancybox-thumb').live('click',function(){
	if ($.browser.msie) {
	alert('Iam clicked');
	}else{
	console.log('Iam clicked');
	}
	if (isMobile) {
		$('.prevNextBarContainer').each(function(){
			$(this).width('10%');
			$(this).children().first().css('font-size','50px');
		})
	}
	changeME($(this));
	// var $outer_container = $("#outer_container");
	// $("body,html").css("overflow", "hidden");
	// $outer_container.width(document.body.clientWidth);
	// $outer_container.css('height', document.body.clientHeight);
	// $outer_container.show();
	// scroll(0, 0);
	// $outer_container.click(function(){
		// $(this).hide();
	// })
	return false;
});