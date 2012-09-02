(function ($) {
	$('.hover-show-btn').live('mouseenter',function(){
		var $hoverShowContainer = $(this).find('.hover-show-container');
		$hoverShowContainer.show();
	})
	$('.hover-show-btn').live('mouseleave',function(){
		var $hoverShowContainer = $(this).find('.hover-show-container');
		$hoverShowContainer.hide();
	})  			
})(jQuery);