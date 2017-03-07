/**
 * Created by sabinemaennel on 01.03.17.
 */
// enable or disable clientside form checking
// - to be better able to test server side form checking:
//   html-form checking can be disabled
// - settings regarding form checking are stored

var client_form_checking = $('#client_form_checking');
var myform = $('form');
var client_form_checking_checked = localStorage.getItem('client_form_checking_checked');

if (client_form_checking_checked === "n") {
    client_form_checking.prop("checked", false);
} else {
    client_form_checking.prop("checked", true);
}

client_form_checking.change(function() {
    if (!$(this).prop("checked")) {
        myform.attr('novalidate', 'novalidate');
        localStorage.setItem('client_form_checking_checked', "n");
    } else {
        myform.removeAttr('novalidate');
        localStorage.setItem('client_form_checking_checked', "y");
    }
});

