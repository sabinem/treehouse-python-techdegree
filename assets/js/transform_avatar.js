// transform avatar
// - a selection is made in a form action field
// - after the selection has been made all other selections are removed

// action selector of the form
var action = $('#id_action');

// form elements to be changed
var form = $('form');
var helptext = $('.helptext');
var button = $('#submit');
var avatar = $('#avatar');
var angle_wrapper = $('#angleWrapperId');
var angle_input = $('#angleInputId');
var image = $('img#avatar');
var crop_left = $('#id_crop_left');
var crop_right = $('#id_crop_right');
var crop_top = $('#id_crop_top');
var crop_bottom = $('#id_crop_bottom');


var remove_unselected = function(){
    action.find('option').not(':selected').remove();
};

var crop_handler = function() {
    // crop image
    // makes use of imageareaselect pack:
    // http://odyniec.net/projects/imgareaselect/
    avatar.show();
    helptext.html("use your mouse to mark an area on the image above for cropping");
    helptext.addClass("activehelp");
    button.html('Crop now');

    // selection
    image.imgAreaSelect({
        handles: true,
        onSelectEnd: function (img, selection) {
            crop_left.val(selection.x1);
            crop_top.val(selection.y1);
            crop_right.val(selection.x2);
            crop_bottom.val(selection.y2);
        }
    });
};

var fabric_handler = function(fb_action) {
    // uses fabric.js
    // rotate or flip image
    if (fb_action == "r") {
        angle_input.show();
        angle_wrapper.show();
        helptext.html("rotate with the slider");
        helptext.addClass("activehelp");
        button.html('rotate now');
    }
    avatar.hide();
    // canvas
    var canvas = new fabric.Canvas('c');

    var imgElement = document.getElementById('avatar');

    var imgInstance = new fabric.Image(imgElement, {
      left: 0,
      top: 0
    });
    canvas.add(imgInstance);
    canvas.renderAll();
    imgInstance.setControlsVisibility({
             mt: false,
             mb: false,
             ml: false,
             mr: false,
             bl: false,
             br: false,
             tl: false,
             tr: false,
             mtr: false
          });
    imgInstance.set("hasRotatingPoint", true);
    imgInstance.lockMovementY = true;
    imgInstance.lockMovementX = true;
    imgInstance.selectable = false;


    $('#angleInputId').change(function() {
        var val = this.value;
        imgInstance.setAngle(val).setCoords();
        canvas.renderAll();
    });
    if (fb_action == "tb") {
        imgInstance.set('flipY', true);
        helptext.html("see a preview below, press 'flip now' to perform the flip");
        helptext.addClass("activehelp");
        button.html('flip now');
    }
    if (fb_action == "lr") {
        imgInstance.set('flipX', true);
        helptext.html("see a preview below, press 'flip now' to perform the flip");
        helptext.addClass("activehelp");
        button.html('flip now');
    }
    canvas.renderAll();

};


var selection_handler = function() {
    // handle selection
    // selected action
    var selection = action.val();
    // possible selections
    var crop = action.find("option[value='c']").val();
    var rotate = action.find("option[value='r']").val();
    var flip_lr = action.find("option[value='lr']").val();
    var flip_tb = action.find("option[value='tb']").val();
    switch(selection) {
        case crop:
            crop_handler();
            remove_unselected();
            break;
        case rotate:
            fabric_handler("r");
            remove_unselected();
            break;
        case flip_lr:
            fabric_handler("lr");
            remove_unselected();
            break;
        case flip_tb:
            fabric_handler("tb");
            remove_unselected();
            break;
    }
};

// initializing the variables in the beginning
angle_input.hide();
angle_wrapper.hide();
avatar.show();
helptext.html("Please chose an action");
helptext.removeClass("activehelp");
button.html('Transform' );

// selection on change of action
action.change(selection_handler);


// handle selection after it has been made
selection_handler();









