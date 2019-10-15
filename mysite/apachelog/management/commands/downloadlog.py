import datetime
import re

import requests
from django.core.management import BaseCommand, CommandError
from tqdm import tqdm

from apachelog.models import ApacheLog


class Command(BaseCommand):
    help = 'Loads a Apache log file, parses data and saves to the database.'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='URL for download log file')

    def handle(self, *args, **options):
        try:
            response = requests.get(options['url'], stream=True)
        except requests.exceptions.RequestException as e:
            raise CommandError(e)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise CommandError(e)

        if response.headers is None:
            raise CommandError('There are no headers in the response.')

        # Regex для общего формата Apache лога.
        parts = [
            r'(?P<host>[\d\.]+)',
            r'\S+',
            r'\S+',
            r'\[(?P<time>.+)\]',
            r'"(?P<method>\w+)\s+(?P<url>\S+).*?"',
            r'(?P<status>\d{3})',
            r'(?P<size>\S+)',
        ]
        pattern = re.compile(r'\s+'.join(parts))

        total_size = int(response.headers.get('content-length', 0))
        batch_size = 1000
        object_list = []
        cnt = 0

        # Обрабатываем данные и сохраняем в БД.
        with tqdm(desc='Progress', total=total_size, ncols=80,
                  unit='KB', unit_scale=True) as p_bar:
            for line in response.iter_lines():
                try:
                    line = line.decode('utf-8')
                except UnicodeError:
                    p_bar.update(len(line) + 1)
                    continue

                match = pattern.match(line)
                if match is not None:
                    match = dict(match.groupdict())
                    match['method'] = match['method'].upper()

                    try:
                        match['time'] = datetime.datetime.strptime(
                            match['time'], '%d/%b/%Y:%H:%M:%S %z')
                    except ValueError:
                        p_bar.update(len(line) + 1)
                        continue

                    if match['size'] == '-':
                        match['size'] = None

                    object_list.append(ApacheLog(**match))
                    cnt += 1

                    if cnt == batch_size:
                        ApacheLog.objects.bulk_create(object_list)
                        object_list = []
                        cnt = 0

                p_bar.update(len(line) + 1)

            ApacheLog.objects.bulk_create(object_list)

        self.stdout.write('Successfully downloaded log file.')
