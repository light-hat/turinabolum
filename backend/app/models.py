import uuid
from django.db import models

# Модель для "Кейса"
class Case(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

# Модель для "Дампа"
class Dump(models.Model):
    DUMP_TYPE_CHOICES = [
        ('disk', 'Disk Dump'),
        ('memory', 'Memory Dump'),
        ('traffic', 'Traffic Dump'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(Case, related_name='dumps', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    upload_time = models.DateTimeField(auto_now_add=True)
    dump_type = models.CharField(max_length=50, choices=DUMP_TYPE_CHOICES)

    def __str__(self):
        return self.name

# Модель для "Устройства"
class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dump = models.ForeignKey(Dump, related_name='devices', on_delete=models.CASCADE)
    host = models.CharField(max_length=255)

    def __str__(self):
        return self.host

# Модель для "Пользователя устройства"
class DeviceUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, related_name='users', on_delete=models.CASCADE)
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.username

# Модель для "Кибератаки"
class CyberAttack(models.Model):
    KILLCHAIN_PHASES = [
        ('reconnaissance', 'Reconnaissance'),
        ('weaponization', 'Weaponization'),
        ('delivery', 'Delivery'),
        ('exploitation', 'Exploitation'),
        ('installation', 'Installation'),
        ('command_and_control', 'Command and Control'),
        ('actions_on_objectives', 'Actions on Objectives'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, related_name='cyberattacks', on_delete=models.CASCADE)
    users = models.ManyToManyField(DeviceUser, related_name='cyberattacks')
    date = models.DateField()
    attacker = models.CharField(max_length=255, blank=True, null=True)
    victim = models.CharField(max_length=255)
    attack_type = models.CharField(max_length=255)
    success = models.BooleanField(default=False)
    justification = models.TextField()
    killchain_phase = models.CharField(max_length=50, choices=KILLCHAIN_PHASES)

    def __str__(self):
        return f"{self.attack_type} on {self.victim}"

# Модель для "Индикатора компрометации"
class CompromiseIndicator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    elastic_id = models.CharField(max_length=255)
    description = models.TextField()
    mitre_tags = models.JSONField(default=dict)

    def __str__(self):
        return self.elastic_id
