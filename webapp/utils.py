from urllib.parse import urljoin, urlparse

from flask import request, url_for


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def get_redirect_target():
    """Определяем есть ли параметр next, или предыдущая страница referrer. и переходим на них если они безопасные
    и не равные текущей странице, чтобы не зацикливаться на одной строанице"""
    for target in [
        request.args.get("next"),
        request.referrer,
        url_for("soglasovanie.index", task_filter="active"),
    ]:
        if not target or target == request.base_url:
            continue
        if is_safe_url(target):
            return target
