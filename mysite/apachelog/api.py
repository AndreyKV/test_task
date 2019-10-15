from django.db.models import Count, Sum

from apachelog.models import ApacheLog

HTTP_METHODS = (
    'OPTIONS', 'GET', 'HEAD', 'POST', 'PUT',
    'PATCH', 'DELETE', 'TRACE', 'CONNECT',
)


def get_number_unique_hosts(queryset=None):
    """Количество уникальных IP адресов."""
    if queryset is None:
        queryset = ApacheLog.objects.all()

    return queryset.values('host').distinct().count()


def get_total_size(queryset=None):
    """Общее количество переданных байт."""
    if queryset is None:
        queryset = ApacheLog.objects.all()

    query = queryset.aggregate(total=Sum('size'))
    return query['total'] or 0


def get_top_hosts(queryset=None, count=10):
    """Топ самых распространенных IP адресов."""
    if queryset is None:
        queryset = ApacheLog.objects.all()

    return queryset.values('host').annotate(
        count=Count('host')).order_by('-count')[:count]


def get_number_http_methods(queryset=None):
    """Статистика по количеству http методов."""
    if queryset is None:
        queryset = ApacheLog.objects.all()

    return queryset.filter(method__in=HTTP_METHODS).values(
        'method').annotate(count=Count('method'))
