//좋아요 싫어요 기능을 위한 자바스크립트 함수
$(".like").click(function(){
    var pk = $(this).attr('name')
    $.ajax({ // .like 버튼을 클릭하면 <새로고침> 없이 ajax로 서버와 통신하겠다.
    type: "POST", // 데이터를 전송하는 방법을 지정
    url: likeUrl, // 통신할 url을 지정
    data: {'pk': pk, 'csrfmiddlewaretoken': csrf_token}, // 서버로 데이터 전송시 옵션
    dataType: "json", // 서버측에서 전송한 데이터를 어떤 형식의 데이터로서 해석할 것인가를 지정, 없으면 알아서 판단
    // 서버측에서 전송한 Response 데이터 형식 (json)
    // {'likes_count': post.like_count, 'message': message }
    success: function(response){ // 통신 성공시 - 동적으로 좋아요 갯수 변경, 유저 목록 변경
        $("#likecount").html(response.like_count);
        $("#dislikecount").html(response.dislike_count);
    },
    error: function(request, status, error){ // 통신 실패시 - 로그인 페이지 리다이렉트
    alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
    },
})
})

$(".commentLike").click(function(){
    var pk = $(this).attr('name')
    $.ajax({ // .like 버튼을 클릭하면 <새로고침> 없이 ajax로 서버와 통신하겠다.
    type: "POST", // 데이터를 전송하는 방법을 지정
    url: commentLikeUrl, // 통신할 url을 지정
    data: {'pk': pk, 'csrfmiddlewaretoken': csrf_token}, // 서버로 데이터 전송시 옵션
    dataType: "json", // 서버측에서 전송한 데이터를 어떤 형식의 데이터로서 해석할 것인가를 지정, 없으면 알아서 판단
    // 서버측에서 전송한 Response 데이터 형식 (json)
    // {'likes_count': post.like_count, 'message': message }
    success: function(response){ // 통신 성공시 - 동적으로 좋아요 갯수 변경, 유저 목록 변경
        $("#likecount_"+pk).html(response.like_count);
        $("#dislikecount_"+pk).html(response.dislike_count);
    },
    error: function(request, status, error){ // 통신 실패시 - 로그인 페이지 리다이렉트
    alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
    },
})
})

$(".dislike").click(function(){
    var pk = $(this).attr('name')
    $.ajax({ // .like 버튼을 클릭하면 <새로고침> 없이 ajax로 서버와 통신하겠다.
    type: "POST", // 데이터를 전송하는 방법을 지정
    url: dislikeUrl, // 통신할 url을 지정
    data: {'pk': pk, 'csrfmiddlewaretoken': csrf_token}, // 서버로 데이터 전송시 옵션
    dataType: "json", // 서버측에서 전송한 데이터를 어떤 형식의 데이터로서 해석할 것인가를 지정, 없으면 알아서 판단
    // 서버측에서 전송한 Response 데이터 형식 (json)
    // {'likes_count': post.like_count, 'message': message }
    success: function(response){ // 통신 성공시 - 동적으로 좋아요 갯수 변경, 유저 목록 변경
        $("#likecount").html(response.like_count);
        $("#dislikecount").html(response.dislike_count);
    },
    error: function(request, status, error){ // 통신 실패시 - 로그인 페이지 리다이렉트
    alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
    },
})
})

$(".commentDislike").click(function(){
    var pk = $(this).attr('name')
    $.ajax({ // .like 버튼을 클릭하면 <새로고침> 없이 ajax로 서버와 통신하겠다.
    type: "POST", // 데이터를 전송하는 방법을 지정
    url: commentDislikeUrl, // 통신할 url을 지정
    data: {'pk': pk, 'csrfmiddlewaretoken': csrf_token}, // 서버로 데이터 전송시 옵션
    dataType: "json", // 서버측에서 전송한 데이터를 어떤 형식의 데이터로서 해석할 것인가를 지정, 없으면 알아서 판단
    // 서버측에서 전송한 Response 데이터 형식 (json)
    // {'likes_count': post.like_count, 'message': message }
    success: function(response){ // 통신 성공시 - 동적으로 좋아요 갯수 변경, 유저 목록 변경
        $("#likecount_"+pk).html(response.like_count);
        $("#dislikecount_"+pk).html(response.dislike_count);
    },
    error: function(request, status, error){ // 통신 실패시 - 로그인 페이지 리다이렉트
    alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
    },
})
})

$(".subComment").click(function(){
    var pk = $(this).attr('name')
    $("#subCommentWrite_"+pk).toggle();
});

$("#commentForm").submit(function(){
    $.ajax({
        data: $(this).serialize(),
        type: "POST",
        url:commentWriteUrl,
        dataType: "json",
        success: function(response){
            location.reload(); 
        },
        error: function(request, status, error){ // 통신 실패시 - 로그인 페이지 리다이렉트
        alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
        },
    })
});

$(".subCommentSubmit").click(function(){
    var form = $(this).closest('form');
    $.ajax({
        data: form.serialize(),
        type: "POST",
        url:subCommentWriteUrl,
        dataType: "json",
        success: function(response){
            location.reload(); 
        },
        error: function(request, status, error){ // 통신 실패시 - 로그인 페이지 리다이렉트
        alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
        },
    })
});