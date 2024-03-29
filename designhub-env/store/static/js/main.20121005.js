(function ($) {
	$('.hover-show-btn').live('mouseenter',function(){
		var $hoverShowContainer = $(this).find('.hover-show-container');
		$hoverShowContainer.show();
	})
	$('.hover-show-btn').live('mouseleave',function(){
		var $hoverShowContainer = $(this).find('.hover-show-container');
		$hoverShowContainer.hide();
	})
	var virtualImgs = new Array();
	$('.toggleImage-container').each(function(){
		var virtualImg = new Image(10,10);
	    var img = $(this).find('img');
	    var replaceUrl = img.attr('data-other');
	    if(replaceUrl !== undefined){
			virtualImg.src= replaceUrl;
			virtualImgs.push(virtualImg); 
		}
	});  		
	$('.toggleImage-container').hover(function() {
	  var img = $(this).find('img');
	  var originalUrl = img.attr('src');
	  var replaceUrl = img.attr('data-other');
	  if(replaceUrl !== undefined){
	  	img.attr('src',replaceUrl);
	  	img.attr('data-other',originalUrl);
	  }
	}, function() {
	  var img = $(this).find('img');
	  var originalUrl = img.attr('src');
	  var replaceUrl = img.attr('data-other');
	  if(replaceUrl !== undefined){
	  	img.attr('src',replaceUrl);
	  	img.attr('data-other',originalUrl);
	  }
	});
	$.ajax({
        url: "/talents/ajax/",
        dataType: 'html',
        success: function(data, textStatus, jqXHR){
        	// console.log(data);
        	$('#talents-ajax-container').html(data);
        }
    }).done(function() { 
       // console.log("done");
    });
	// talents-ajax-container
	$('#navbar-header0').delegate('#drop4', 'mouseover', function(event) {
		var self = $(this),
		    title = self.find('a').first(),
		    // preview = self.find('div.preview'),
			submenu = self.find('ul.subnav0');
 
		// If we can't find a sub-menu... return
		if(!submenu.length) { 
			// console.log('cannot find');
		return false; }
        submenu.first().show();

	});
	$('#navbar-header0').delegate('#drop4', 'mouseleave', function(event) {
		var self = $(this),
		    title = self.find('a').first(),
		    // preview = self.find('div.preview'),
			submenu = self.find('ul.subnav0');
 
		// If we can't find a sub-menu... return
		if(!submenu.length) { 
			// console.log('cannot find');
			return false;
        }
        submenu.first().hide();

	});
    function FauxPlaceholder() {
        if(!ElementSupportAttribute('input','placeholder')) {
            $("input[placeholder]").each(function() {
                var $input = $(this);
		        var originalColor = $input.css('color');
		        var placeholderColor = '#bbb';
                $input.after('<input id="'+$input.attr('id')+'-faux" style="display:none;" type="text" value="' + $input.attr('placeholder') + '" />');
                var $faux = $('#'+$input.attr('id')+'-faux');

                $faux.show().attr('class', $input.attr('class')).attr('style', $input.attr('style'));
                $faux.css('color',placeholderColor);    
                $input.hide();

                $faux.focus(function() {
                    $faux.hide();
                    $input.show().focus();
                    $input.css('color',originalColor);   
                });

                $input.blur(function() {
                    if($input.val() === '') {
                        $input.hide();
                        $faux.show();
                        $faux.css('color',placeholderColor);   
                    }
                });
            });
        }
    }
    function ElementSupportAttribute(elm, attr) {
        var test = document.createElement(elm);
        return attr in test;
    }
    FauxPlaceholder();	
})(jQuery);