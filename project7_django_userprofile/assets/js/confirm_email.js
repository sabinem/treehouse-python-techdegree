/**
 * Created by sabinemaennel on 28.02.17.
 */
// Expects an email input field and an email confirmation field
// The confirmation field is shown if the email field changes
//
// html:
// <input id="id_email">
// <div>
// <input id="id_email_confirm" >
// </div>
//
// css:
// .no_confirm_needed {display: none;}
//
// wrapper has class error if 'error' occurs during the confirmation

var email_field = $('#id_email');
var confirm_wrapper = $('#id_email_confirm').parent();

confirm_wrapper.addClass('no_confirm_needed');

email_field.change(function(){
    confirm_wrapper.removeClass('no_confirm_needed');
});

if (confirm_wrapper.hasClass('error')) {
    confirm_wrapper.removeClass('no_confirm_needed');
}
