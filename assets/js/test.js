
   var email_input_field_wrapper = email_input_field.parent();
   email_input_field.change(function(){
      email_confirm_field_wrapper.show();
   });

   if (email_input_field_wrapper.has('error')) {
      email_confirm_field_wrapper.show();
   }   /**
 * Created by sabinemaennel on 20.02.17.
 */
