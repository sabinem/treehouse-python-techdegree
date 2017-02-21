$( document ).ready(function(){

   // fieldWrappers of error fields
   var error_field_wrapper = $('ul.errorlist').parent();
   // the form
   var form = $('form');

   // add error class to error field_wrappers
   error_field_wrapper.addClass('error');

   // first error field wrapper on page
   var first_error_field_wrapper = $('.fieldWrapper.error').first();

   // focus on the input field of it
   if (first_error_field_wrapper.has('textarea')){
      first_error_field_wrapper.find('textarea').focus();
   }
   if (first_error_field_wrapper.has('input')){
      first_error_field_wrapper.find('input').focus();
   }

   // email confirmation field wrapper
   var email_confirm_field_wrapper = $('#id_email_confirm').parent();
   email_confirm_field_wrapper.addClass('no_confirm_needed');

   // email_field_wrapper
   var email_input_field = $('#id_email');
   email_input_field.change(function(){
      email_confirm_field_wrapper.removeClass('no_confirm_needed');
   });
      if (email_confirm_field_wrapper.hasClass('error')) {
      email_confirm_field_wrapper.removeClass('no_confirm_needed');
   }

});

