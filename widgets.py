from wtforms import widgets

import json
from wtforms.widgets import Select, HTMLString, html_params, TextArea
from wtforms.compat import text_type
from html import escape


class TimeInput(widgets.Input):
    input_type = 'time'


class DateInput(widgets.Input):
    input_type = 'date'


class ChosenSelect(Select):
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
    """
    def __init__(self, cssid=None):
        super().__init__()
        self.cssid = cssid

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html= []
        html.append(super().__call__(field, **kwargs))
        html.append("<script>var simplemde = new SimpleMDE({element: $('#%s')});</script>\n" % self.cssid)

        return HTMLString('\n'.join(html))
