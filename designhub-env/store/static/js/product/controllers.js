var AppRouter = Backbone.Router.extend({
	restfulUrl:"/api/comment/product/" + productid + "/", 
    routes : {
        "" : "fun1"//,
        // "modal/product:id" : 'modalProduct'
    },
    fun1 : function (par) {
        $.ajax({
            url: this.restfulUrl,
            data: {page: 1,limit:5,format:'json'},
            dataType:'json',
            success:function (data, textStatus, jqXHR) {
                 this.comments = new Comments(data);
                 /*alert(JSON.stringify(this.comments));*/
                 this.comment_view = new CommentView({model:this.comments});
                 this.comment_view.render();
             }
        });
    }
})