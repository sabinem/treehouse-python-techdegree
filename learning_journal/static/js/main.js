// Chosen module
$(function() {
    $(".chzn-select").chosen();
});

// Simple MDE Editor for Markdown
$(function() {
    $('textarea').each(function () {
        var simplemde = new SimpleMDE({
            element: this
        });
        simplemde.render();
    });
});

// chosen-select: show instruction, when
// there are no choices yet
$(document).ready(function(){
    $("#resources_chosen input").focus(function(){
        $("#notification-resources").css("display", "inline");
    });
    $("#resources_chosen input").focusout(function(){
        $("#notification-resources").css("display", "none");
    });
    $("#tags_chosen input").focus(function(){
        $("#notification-tags").css("display", "inline");
    });
    $("#tags_chosen input").focusout(function(){
        $("#notification-tags").css("display", "none");
    });
});
