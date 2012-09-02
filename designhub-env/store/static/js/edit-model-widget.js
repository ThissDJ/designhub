$(function(){
	
	
	$('.designer-thumb').live('mouseenter',function(){
		var designer_slug = $(this).attr('data-slug');
		if($(this).find('div.widget-panel').length === 0){
			var widget_panel_html = "<div class='widget-panel'>" 
			                         + "<a href='/admin-designer/update/"
			                        + designer_slug +"/'>"
			                 + "modify" + "</a>"
			                 + "<a href='/admin-designer/delete/"
			                        + designer_slug +"/'>"
			                 + "delete" + "</a>"
			                 +  "</div>";
			var widget_panel_underneath_html = "<div class='widget-panel-underneath'>"
			                 +  "</div>";
			$(this).append(widget_panel_html);
			$(this).append(widget_panel_underneath_html);
		}else{
			$widget_panel = $(this).find('div.widget-panel').eq(0);
			$widget_panel.show();
			$widget_panel_underneath = $(this).find('div.widget-panel-underneath').eq(0);
			$widget_panel_underneath.show();
		}
	});
	$('.designer-thumb').live('mouseleave',function(){
		$widget_panel = $(this).find('div.widget-panel').eq(0);
        $widget_panel.hide();
		$widget_panel_underneath = $(this).find('div.widget-panel-underneath').eq(0);
        $widget_panel_underneath.hide();
	});
		
	
});