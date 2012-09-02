$(function() {
    $('#join-us-ajaxForm').ajaxForm({
    	success: function(data, textStatus, jqXHR){
    		        $( "#dialog p").html(data);
        	        $( "#dialog" ).dialog();
                 }
    }); 
});