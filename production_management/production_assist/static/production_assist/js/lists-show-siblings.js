$(document).ready(function () {
    $('div ol > li:first-child').on('click', function () {
            console.log('click', $(this));
            $(this).siblings().toggleClass('d-none');
            return false;
    });
});