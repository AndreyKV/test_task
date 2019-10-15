from django.db.models import Q
from django.views.generic import ListView

from apachelog import api
from apachelog.models import ApacheLog


class ApacheLogListView(ListView):
    model = ApacheLog
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(host__icontains=search) | Q(time__icontains=search) |
                Q(method__icontains=search) | Q(url__icontains=search) |
                Q(status__icontains=search) | Q(size__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Дополняем контекст данными статистики.
        context['top_hosts'] = api.get_top_hosts(self.object_list)
        context['num_methods'] = api.get_number_http_methods(self.object_list)
        context['info'] = [
            {
                'name': 'Количество уникальных IP адресов',
                'value': api.get_number_unique_hosts(self.object_list),
            },
            {
                'name': 'Общее число переданных байт',
                'value': api.get_total_size(self.object_list),
            },
        ]

        return context
