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