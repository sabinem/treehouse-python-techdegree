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

