/**
 * Created by sabinemaennel on 28.02.17.
 */
// custom styling of form error
// - puts the focus to the first detected error field
// - this may be a textarea or an input field
// - wrappers of errors receive also the css class 'error'    
    

var form = $('form');
var error_field_wrapper = $('ul.errorlist').parent();
var first_error_field_wrapper = $('.fieldWrapper.error').first();

error_field_wrapper.addClass('error');

if (first_error_field_wrapper.has('textarea')){
  first_error_field_wrapper.find('textarea').focus();
}

if (first_error_field_wrapper.has('input')){
  first_error_field_wrapper.find('input').focus();
}

