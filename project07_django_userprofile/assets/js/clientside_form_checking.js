/**
 * Created by sabinemaennel on 01.03.17.
 */
// enable or disable clientside form checking
// - to be better able to test server side form checking:
//   html-form checking can be disabled

jQuery(function($) {
    var myform = $('form');
    var form_check_stored = localStorage.getItem('form_checking');
    var form_checkbox = $("#chk");
    if (form_check_stored == "yes") {
        form_checkbox.prop("checked", true);
        myform.removeAttr('novalidate');
    } else {
        form_checkbox.prop("checked", false);
         myform.attr('novalidate', 'novalidate');
    }

    form_checkbox.change(function() {
        var isChecked = $(this).is(":checked") ? "yes" : "no";
        localStorage.setItem('form_checking', isChecked);

        if (isChecked == "yes") {
            myform.removeAttr('novalidate');
        } else {
            myform.attr('novalidate', 'novalidate');
        }
    })
});