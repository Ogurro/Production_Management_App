$(document).ready(function () {
    console.log('ready');
    $('div ol li:first-child').on('click', function (element) {
        $(this).siblings().toggleClass('d-none');
        return false
    })
});