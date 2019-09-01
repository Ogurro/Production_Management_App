$(document).ready(function () {
    // add label
    let formP = $('form p').addClass("form-group d-inline-block");
    let formPInput = formP.children('input').addClass('form-control');
    [].forEach.call(formPInput, function (element) {
        let name = element.getAttribute('name');
        if (name) {
            name = name[0].toUpperCase() + name.slice(1);
        }
        element.setAttribute('placeholder', name.replace('\_', '\ '));
    });
    formPInput.wrap('<div class="col-lg-auto input-group-lg d-inline-flex"></div>');
    formP.children('label').addClass('lead font-weight-bold');

    // text area
    let textAreaInput = $('p textarea');
    textAreaInput.addClass('form-control');
    textAreaInput.wrap('<div class="col-sm-auto col-lg-auto input-group-lg d-inline-flex"></div>');

    // custom checkbox
    let checkboxInput = $('p input[type="checkbox"]');
    checkboxInput.toggleClass('form-control form-check-input mt-2 ml-0 my-checkbox');
    checkboxInput.parent().toggleClass('d-inline-flex d-inline');

    // errors
    let errorList = $('ul.errorlist');
    errorList.addClass('list-group mb-2 mt-2');
    errorList.children('li').addClass('list-group-item list-group-item-warning col-lg-4 col-sm-10');

    // show search
    let showSearchButton = $('button#show-search');
    showSearchButton.on('click', function () {
        $(this).toggleClass('btn-secondary btn-success');
        $(this).next('form').toggleClass('d-none');
    });

    // clear button
    let clearButton = $('input#clear');
    clearButton.on('click', function () {
        formPInput.attr('value', formPInput.val());
        formPInput.val('');
        formPInput.attr('value', '');
    });
});