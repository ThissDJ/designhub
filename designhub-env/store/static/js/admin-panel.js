$(function() {
    $("#hide-admin").live('click',function(){
    	$("#admin-panel").hide();
    	$("#show-admin-panel").show();
    	return false;
    });
    $("#show-admin").live('click',function(){
    	$("#admin-panel").show();
    	$("#show-admin-panel").hide();
    	return false;
    });
});