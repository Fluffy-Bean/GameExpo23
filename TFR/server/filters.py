import datetime
from flask import Blueprint


blueprint = Blueprint('filters', __name__, template_folder='templates')


@blueprint.app_template_filter()
def format_result(dttm):
    dttm = str(dttm).split('.')
    time = datetime.timedelta(seconds=int(dttm[0]))
    microtime = dttm[1][:3]
    return f'{time}:{microtime}'
