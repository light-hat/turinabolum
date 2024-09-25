import subprocess

# Параметры для вызова log2timeline
log2timeline_cmd = [
    'log2timeline',
    '--storage-file', 'my_storage_file.plaso',
    '--partitions', 'all',
    'ARM1.vmdk'
]

# Выполняем команду
subprocess.run(log2timeline_cmd)

# Параметры для вызова psort
psort_cmd = [
    'psort',
    '--output-format', 'l2tcsv',
    'my_storage_file.plaso',
    '-w', 'output.csv'
]

# Выполняем команду
subprocess.run(psort_cmd)
