$(document).ready(function () {
    $('button#personnel').on('click', function () {
        $(this).next().toggleClass('d-none');
    });
    $('button#retail').on('click', function () {
        $(this).next().toggleClass('d-none');
    });
});