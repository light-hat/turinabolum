import subprocess
from celery import shared_task
from .models import Dump, Device, DeviceUser
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://elasticsearch:9200'])

@shared_task
def process_disk_dump(dump_id):
    dump = Dump.objects.get(id=dump_id)

    # Параметры для вызова log2timeline
    log2timeline_cmd = [
        'log2timeline',
        '--storage-file', 'my_storage_file.plaso',
        '--partitions', 'all',
        dump.name  # Предполагается, что путь к файлу дампа указан в поле name
    ]

    subprocess.run(log2timeline_cmd)

    # Параметры для вызова psort
    psort_cmd = [
        'psort',
        '--output-format', 'l2tcsv',
        'my_storage_file.plaso',
        '-w', 'output.csv'
    ]

    subprocess.run(psort_cmd)

    # Обработка CSV-файла и сохранение событий в Elasticsearch
    with open('output.csv', 'r') as f:
        next(f)  # Пропускаем заголовок CSV
        for line in f:
            fields = line.strip().split(',')
            event = {
                "date": fields[0],
                "time": fields[1],
                "timezone": fields[2],
                "MACB": fields[3],
                "source": fields[4],
                "sourcetype": fields[5],
                "type": fields[6],
                "user": fields[7],
                "host": fields[8],
                "short": fields[9],
                "desc": fields[10],
                "version": fields[11],
                "filename": fields[12],
                "inode": fields[13],
                "notes": fields[14],
                "format": fields[15],
                "extra": fields[16]
            }
            es.index(index='plaso_events', body=event)

            # Создаем устройство и пользователя на основе данных
            device, created = Device.objects.get_or_create(dump=dump, host=event['host'])
            DeviceUser.objects.get_or_create(device=device, username=event['user'])
