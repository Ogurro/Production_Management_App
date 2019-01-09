$(document).ready(function () {
    $('p#personnel').on('click', function () {
        $(this).next().toggleClass('d-none');
    });
    $('p#retail').on('click', function () {
        $(this).next().toggleClass('d-none');
    });
});