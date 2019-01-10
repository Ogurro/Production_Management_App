$(document).ready(function () {
    $('div ol > li:first-child').on('click', function () {
            $(this).siblings().toggleClass('d-none');
            return false;
    });
});