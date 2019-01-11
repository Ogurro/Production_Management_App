$(document).ready(function () {
    // add label
    let form_p = $('form p').addClass("form-group");
    let form_p_input = form_p.children('input').addClass('form-control');
    [].forEach.call(form_p_input, function (element) {
        let name = element.getAttribute('name');
        if (name) {
            name = name[0].toUpperCase() + name.slice(1);
        }
        element.setAttribute('placeholder', name.replace('\_', '\ '));
    });
    form_p_input.wrap('<div class="col-sm-10 col-lg-4 input-group-lg d-inline-flex"></div>');
    form_p.children('label').addClass('lead font-weight-bold');

    // text area
    let textAreaInput = $('p textarea');
    textAreaInput.addClass('form-control');
    textAreaInput.wrap('<div class="col-sm-10 col-lg-auto input-group-lg d-inline-flex"></div>');

    // custom checkbox
    let checkboxInput = $('p input[type="checkbox"]');
    checkboxInput.toggleClass('form-control form-check-input mt-2 ml-0 my-checkbox');
    checkboxInput.parent().toggleClass('d-inline-flex d-inline');

    // errors
    let errorList = $('ul.errorlist');
    errorList.addClass('list-group mb-2 mt-2');
    errorList.children('li').addClass('list-group-item list-group-item-warning col-lg-4 col-sm-10');
});