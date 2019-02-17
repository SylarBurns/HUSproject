$(function () {
    $('#sideMenu').each(function () {

        var $window = $(window), 
            $header = $(this), 
            headerOffsetTop = $header.offset().top;

        $window.on('scroll', function () {
            if ($window.scrollTop() > headerOffsetTop) {
                $header.addClass('sticky');
            } else {
                $header.removeClass('sticky');
            }
        });
        $window.trigger('scroll');

    });
});

function openTab(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}


$(".delete").click(function(){
    var pk = $(this).attr('value')
    $.ajax({ // .delete 버튼을 클릭하면 <새로고침> 없이 ajax로 서버와 통신하겠다.
    type: "POST", // 데이터를 전송하는 방법을 지정
    url: deleteNoticeUrl, // 통신할 url을 지정
    data: {'pk': pk, 'csrfmiddlewaretoken': csrf_token}, // 서버로 데이터 전송시 옵션
    dataType: "json", // 서버측에서 전송한 데이터를 어떤 형식의 데이터로서 해석할 것인가를 지정, 없으면 알아서 판단
    // 서버측에서 전송한 Response 데이터 형식 (json)

    success: function(response){ // 통신 성공시 
        location.reload();
    },
    error: function(request, status, error){ // 통신 실패시 - 로그인 페이지 리다이렉트
    alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
    },
})
})
$(".deleteAll").click(function(){
    var pk = $(this).attr('value')
    $.ajax({ // .delete 버튼을 클릭하면 <새로고침> 없이 ajax로 서버와 통신하겠다.
    type: "POST", // 데이터를 전송하는 방법을 지정
    url: deleteAllUrl, // 통신할 url을 지정
    data: {'csrfmiddlewaretoken': csrf_token}, // 서버로 데이터 전송시 옵션
    dataType: "json", // 서버측에서 전송한 데이터를 어떤 형식의 데이터로서 해석할 것인가를 지정, 없으면 알아서 판단
    // 서버측에서 전송한 Response 데이터 형식 (json)
    success: function(response){ // 통신 성공시 
        location.reload()
    },
    error: function(request, status, error){ // 통신 실패시 - 로그인 페이지 리다이렉트
    alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
    },
})
})



$(function(){
    $(window).load(function(){
        $('.ajaxProgress').fadeOut(2000);
    })
});

$(window).on('load', function () {
    $("#loader").fadeOut(1000)
});

