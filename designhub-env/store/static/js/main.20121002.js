(function ($) {
	$('.hover-show-btn').live('mouseenter',function(){
		var $hoverShowContainer = $(this).find('.hover-show-container');
		$hoverShowContainer.show();
	})
	$('.hover-show-btn').live('mouseleave',function(){
		var $hoverShowContainer = $(this).find('.hover-show-container');
		$hoverShowContainer.hide();
	})  		
	$('.toggleImage-container').hover(function() {
	  var img = $(this).find('img');
	  var originalUrl = img.attr('src');
	  var replaceUrl = img.attr('data-other');
	  if(typeof replaceUrl !== undefined){
	  	img.attr('src',replaceUrl);
	  	img.attr('data-other',originalUrl);
	  }
	}, function() {
	  var img = $(this).find('img');
	  var originalUrl = img.attr('src');
	  var replaceUrl = img.attr('data-other');
	  if(typeof replaceUrl !== undefined){
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
})(jQuery);