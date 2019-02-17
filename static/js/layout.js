// //gnb
// $(document).ready(function(){
// 	var $gnbLi=$('#gnb>ul>li');
// 	var $gnbSub=$('#gnb>ul>li>ul');
// 	$gnbLi.mouseenter(function(){
// 		$(this).find('ul').show();
// 	});
// 	$gnbLi.mouseleave(function(){
// 		$gnbSub.hide();
// 	});
// });

//tab
$(function() { 
	$(".tab_content").hide(); 
	$(".tab_content:first").show(); 

	$("ul.tabs li").click(function() { 
	$("ul.tabs li").removeClass("active").css("color","#5e5e5e"); 
	//$(this).addClass("active").css({"color": "darkred","font-weight": "bolder"}); 
	$(this).addClass("active").css("color","#fff"); 
	$(".tab_content").hide() 
	var activeTab = $(this).attr("rel"); 
	$("#"+activeTab).fadeIn() 
	}); 
}); 

//tb_data
$(document).ready(function(e) {
    $('.tb_data tr:nth-child(odd)').addClass('odd');
});


$(function () {
    $('.page-header').each(function () {

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


$(document).ready(function(){
	$('#bt_gnb').click(function(e) {
		 $(this).toggleClass('on');
	   $('#gnb').toggleClass('on');
	 });
	 $('#bt_search').click(function(e) {
	  $('#hsearch').toggleClass('on');
	});
	$('#gnb ul li span').click(function(e) {
		$(this).parent().toggleClass('on');
		$(this).parent().siblings().removeClass('on');
	});
 });

 $(document).ready(function() {
    $(".bestFive_info_content").hide();
    $("ul.bestFive_info li:first").addClass("active").show();
    $(".bestFive_info_content:first").show();
    $("ul.bestFive_info li").click(function() {
        $("ul.bestFive_info li").removeClass("active");
        $(this).addClass("active");
        $(".bestFive_info_content").hide();
        var activeTab = $(this).find("a").attr("href");
        $(activeTab).show();
        return false;
    });
});

$(document).ready(function() {
    $(".market_info_content").hide();
    $("ul.market_info li:first").addClass("active").show();
    $(".market_info_content:first").show();
    $("ul.market_info li").click(function() {
        $("ul.market_info li").removeClass("active");
        $(this).addClass("active");
        $(".market_info_content").hide();
        var activeTab = $(this).find("a").attr("href");
        $(activeTab).show();
        return false;
    });
});

$(document).ready(function() {
    $(".lostAndFound_info_content").hide();
    $("ul.lostAndFound_info li:first").addClass("active").show();
    $(".lostAndFound_info_content:first").show();
    $("ul.lostAndFound_info li").click(function() {
        $("ul.lostAndFound_info li").removeClass("active");
        $(this).addClass("active");
        $(".lostAndFound_info_content").hide();
        var activeTab = $(this).find("a").attr("href");
        $(activeTab).show();
        return false;
    });
});

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

$(document).ready(function() {
    $("submenu").hide();
    $("ul.sideGnb ul:first").show()
    $("ul.sideGnb li").click(function() {
        var activeTab = $(this).find("a").attr("href");
        $(activeTab).toggle();
        return false;
    });
});