$(document).ready(function(){

    $(".subComment").click(function(){
        var pk = $(this).attr('name')
        $("#subCommentWrite_"+pk).toggle();
    });
  });

$(function(){
    $("#subComment_"+pk).click(function(){
        $(".boardName").hide();
    });
});