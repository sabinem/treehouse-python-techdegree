
import jinja2
import flask

blueprint = flask.Blueprint('filters', __name__)

# using the decorator
@jinja2.contextfilter
@blueprint.app_template_filter()
def filter1(context, value):
    return 1

# using the method
@jinja2.contextfilter
def filter2(context, value):
    return 2

blueprint.add_app_template_filter(filter2)