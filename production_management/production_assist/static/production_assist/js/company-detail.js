$(document).ready(function () {
    $('button#personnel').on('click', function () {
        $(this).siblings('div.container').toggleClass('d-none');
    });
    $('button#retail').on('click', function () {
        $(this).siblings('div.container').toggleClass('d-none');
    });
});