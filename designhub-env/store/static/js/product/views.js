function setNewLimit(urlpath){
	return urlpath.replace(/limit\=\d+/gi,'limit=10');
}
var commentLimit = 4;
var CommentView = Backbone.View.extend({
	el : $("#comment_container_container"),
    tagName : "div",

    initialize: function () {
        this.model.bind('change', this.render, this);
       // alert(this.render().el);
    },
    
    events: {
	    "click .more-comments" : "showMoreComments",
	    "click .post-comment-btn" : "postComment"
    },
    
    render: function () {
    	var comment_template= _.template($("#CommentTemplate").html());
        var hide_comment_template = _.template($("#HideCommentTemplate").html());
        
        if(this.model.get('total') > 0){
        	var that = this;
        	
        	$(this.el).find('.comment_container').first().html(function(){
        		if(that.model.get('total') < 3){
        		    var return_html = that.model.get('results').map(function(item,index,array){
				        		     return comment_template(item);
				        	 }).join('');
        			return return_html
        		}else{
        		    var return_html = that.model.get('results').map(function(item,index,array){
	        		    	if(index < 2){
	        		    		return comment_template(item);
	        		    	}else{
	        		    		return hide_comment_template(item);
	        		    	}    
				        }).join('');
        			var more_comment_template = _.template($("#MoreCommentTemplate").html());
	        		return return_html + more_comment_template();
        		}
        	});
        }
        return this;
    },
    showMoreComments : function(){
    	var moreCommentsEl = $(this.el).find('.more-comments');
    	if(moreCommentsEl.hasClass('not-clicked-yet')){
    		moreCommentsEl.removeClass('not-clicked-yet');
    		moreCommentsEl.parent().parent().find('.hide-comment').removeClass('hide');
    		if(this.model.get('next') === null){
    			moreCommentsEl.parent().remove();
    		}
    	}else{
    		var that = this;
	        $.ajax({
	            url: this.model.get('next'),
	            data: {format:'json'},
	            dataType:'json',
	            success:function (data, textStatus, jqXHR) {
	            	var comment_template = _.template($("#CommentTemplate").html());
	            	var return_html = data.results.map(function(item,index,array){
			        		     return comment_template(item);
			        	 }).join('');
			        moreCommentsEl.parent().before(return_html);
			        if(data.next === null){
			        	moreCommentsEl.parent().remove();
			        }
			        that.model.next = data.next;
	             }
	        });
    	}
    },
    postComment : function(){
    		var that = this;
    		var postCommentTextarea = $(this.el).find('.post-comment-textarea');
            var comment_container = $(this.el).find('.comment_container');
	        $.ajax({
	            url: '/api/comment/',
	            data: {product:productid
	                       ,content:postCommentTextarea.val()
	                  },
	            dataType:'json',
	            type: 'POST',
	            success:function (data) {
	            	//console.log(data);
	            	var comment_template = _.template($("#CommentTemplate").html());
	            	var return_html = comment_template(data);
	            	var comment_container_firstChild = comment_container.children().eq(0);
	            	console.log(comment_container_firstChild.html());
	            	comment_container_firstChild.before(return_html);
	            	postCommentTextarea.val('');
	            	if(comment_container_firstChild.hasClass('no-any-comment')){
	            		comment_container_firstChild.remove();
	            	}
	             }
	        });
	        return false;
    }
});
/*var ProductSetView = Backbone.View.extend({
    el : $("#products-container"),
    initialize : function (model, options) {
        this.model.bind("change", this.render, this);
        this.render();
    },

    render : function () {
        var self = this;
        $(self.el).empty();
        _.each(this.model.models, function (product) {
	        $.ajax({
	            url: '/api/comment/product/' + product.id + '/',
	            data: {page: 1,limit:commentLimit,format:'json'},
	            dataType:'json',
	            success:function (data, textStatus, jqXHR) {
	                 product.comments = data;
	                 product.open_div_id = '#modal-product' + product.id;
	                 $(self.el).append(  new ProductView({model:product}).render().el);
	             }
	        });
        })
       return self;
    }
});*/
