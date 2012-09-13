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
})(jQuery);