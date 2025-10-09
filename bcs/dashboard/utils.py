# dashboard/utils.py
from django.conf import settings
from django.urls import get_resolver, URLPattern, URLResolver


def get_project_apps():
    """
    Return only project apps (filtering out Django/third-party).
    Adjust filtering as needed.
    """
    excluded_prefixes = ("django", "dal", "dj", "nested")
    return sorted(
        [
            app.split(".")[-1]  # use short name
            for app in settings.INSTALLED_APPS
            if not app.startswith(excluded_prefixes)
        ]
    )


def list_named_urls(resolver=None, prefix=""):
    if resolver is None:
        resolver = get_resolver()
    urls = []

    for pattern in resolver.url_patterns:
        if isinstance(pattern, URLPattern) and pattern.name:
            full_name = (
                f"{prefix}{pattern.name}" if prefix else str(pattern.name)
            )
            urls.append(full_name)
        elif isinstance(pattern, URLResolver):
            ns_prefix = (
                f"{prefix}{pattern.namespace}:"
                if pattern.namespace
                else prefix
            )
            urls.extend(list_named_urls(pattern, ns_prefix))
    return list(set(urls))
