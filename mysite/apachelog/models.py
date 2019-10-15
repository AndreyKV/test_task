from django.db import models


class ApacheLog(models.Model):
    """
    Модель для представления данных Apache лога.
    """
    host = models.GenericIPAddressField('IP address')
    time = models.DateTimeField('Time')
    method = models.CharField('HTTP method', max_length=10)
    url = models.URLField('URL')
    status = models.CharField('Status', max_length=3)
    size = models.PositiveIntegerField('Size', null=True, blank=True)

    class Meta:
        verbose_name = 'Apache log'
        verbose_name_plural = 'Apache log'

        indexes = [
            models.Index(fields=['host', 'time', 'method'])
        ]

    def __str__(self):
        return '{} {} {}'.format(self.host, self.time, self.method)
