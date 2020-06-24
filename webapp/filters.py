import pytz


def register_my_jinja_filters(app):
    @app.template_filter('datetime_vl')
    def datetime_vl(value):
        """ Фильтр даты для фласка, преобразует дату UTC в временную зону Владивостока"""

        DATE_FORMAT = '%d.%m.%Y %H:%M'

        tz_utc = pytz.utc
        tz_vl = pytz.timezone('Asia/Vladivostok')
        value = tz_utc.localize(value, is_dst=None)
        local_dt = value.astimezone(tz_vl)

        return local_dt.strftime(DATE_FORMAT)