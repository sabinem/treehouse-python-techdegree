"""
This file includes custom widgests for wt-forms
"""
import json

from wtforms import widgets
from wtforms.widgets import Select, HTMLString, TextArea


class TimeInput(widgets.Input):
    """
    Time input widget
    """
    input_type = 'time'


class DateInput(widgets.Input):
    """
    Date input widget
    """
    input_type = 'date'


class ChosenSelect(Select):
    """
    widget for chosen js field
    """
    def __init__(self, multiple=False, renderer=None):
        super(ChosenSelect, self).__init__(multiple=multiple)
        self.renderer = renderer
        options = {}
        options.setdefault('width', '100%')
        self.options = options

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = []
        html.append(super().__call__(field, **kwargs))
        html.append(
            '<script>$("#%s").chosen(%s);</script>\n'
            % (kwargs['id'], json.dumps(self.options))
        )
        return HTMLString('\n'.join(html))


class MarkupTextArea(TextArea):
    """
    Renders a multi-line text area.
    `rows` and `cols` ought to be passed as keyword args when rendering.
    uses the SimpleMDE Editor
    """
    def __init__(self, cssid=None):
        super().__init__()
        self.cssid = cssid

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = []
        html.append(super().__call__(field, **kwargs))
        html.append("<script>var simplemde "
                    "= new SimpleMDE({element: $('#%s')});</script>\n"
                    % self.cssid)
        return HTMLString('\n'.join(html))
