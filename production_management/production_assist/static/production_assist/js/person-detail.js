$(document).ready(function () {
    $('button#offers').on('click', function () {
        $(this).next().toggleClass('d-none');
    });
});