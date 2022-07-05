from datetime import datetime, timedelta

import pytz


def register_my_jinja_filters(app):
    @app.template_filter("datetime_vl")
    def datetime_vl(value, fmt=None):
        """Фильтр даты для фласка, преобразует дату UTC в временную зону Владивостока"""

        if not value:
            return value

        if not fmt:
            fmt = "%d.%m.%Y %H:%M"

        tz_utc = pytz.utc
        tz_vl = pytz.timezone("Asia/Vladivostok")
        value = tz_utc.localize(value, is_dst=None)
        local_dt = value.astimezone(tz_vl)

        return local_dt.strftime(fmt)

    @app.template_filter("is_later_than_n_days")
    def is_later_than_n_days(date, n_days):
        if not date:
            return False
        return  (datetime.now() - date) > timedelta(days=n_days)
