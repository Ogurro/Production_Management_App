$(document).ready(function () {
    let form_p = $('form p').addClass("form-group");
    let form_p_input = form_p.children('input').addClass('form-control');
    [].forEach.call(form_p_input, function (element) {
        let name = element.getAttribute('name');
        if (name) {
            name = name[0].toUpperCase() + name.slice(1)
        }
        element.setAttribute('placeholder', name);
    });
    form_p_input.wrap('<div class="col-sm-10 col-lg-3 input-group-lg d-inline-flex"></div>');
    form_p.children('label').addClass('col-form-label col-lg-1 pl-0');
});