import uuid
from django.db import models


OBJECT_STATUS_CHOICES = [
    ('processing', 'В обработке'),
    ('ready', 'Готово'),
    ('error', 'Ошибка анализа'),
]

class Case(models.Model):
    """
    Модель, описывающая кейс.
    Кейс отвечает за определённое расследование.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=600)
    description = models.TextField()

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Кейсы"
        verbose_name = "Кейс"

    def __str__(self):
        return self.name


class Dump(models.Model):
    """
    Модель, описывающая выбранный на обработку дамп.
    """
    DUMP_TYPE_CHOICES = [
        ('disk', 'Disk Dump'),
        ('memory', 'Memory Dump'),
        ('traffic', 'Traffic Dump'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(Case, related_name='dumps', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=OBJECT_STATUS_CHOICES)
    filename = models.CharField(max_length=600)
    upload_time = models.DateTimeField(auto_now_add=True)
    dump_type = models.CharField(max_length=50, choices=DUMP_TYPE_CHOICES)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Дампы"
        verbose_name = "Дамп"

    def __str__(self):
        return self.filename


class Device(models.Model):
    """
    Модель, описывающая устройство, задействованное в расследовании.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dump = models.ForeignKey(Dump, related_name='devices', on_delete=models.CASCADE)
    host = models.CharField(max_length=600)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Устройства"
        verbose_name = "Устройство"

    def __str__(self):
        return self.host


class DeviceUser(models.Model):
    """
    Пользователь устройства, задействованного в расследовании.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, related_name='users', on_delete=models.CASCADE)
    username = models.CharField(max_length=600)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Пользователи устройств"
        verbose_name = "Пользователь устройства"

    def __str__(self):
        return self.username


class CyberAttack(models.Model):
    """
    Модель оформляемой аналитиком атаки.
    """
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
    attacker = models.CharField(max_length=600, blank=True, null=True)
    victim = models.CharField(max_length=600)
    attack_type = models.CharField(max_length=600)
    success = models.BooleanField(default=False)
    justification = models.TextField()
    killchain_phase = models.CharField(max_length=50, choices=KILLCHAIN_PHASES)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Атаки"
        verbose_name = "Атака"

    def __str__(self):
        return f"{self.attack_type} on {self.victim}"


class CompromiseIndicator(models.Model):
    """
    Модель автоматически обнаруженного идентификатора компрометации.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    elastic_id = models.CharField(max_length=600)
    description = models.TextField()
    mitre_tags = models.CharField(max_length=600)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "IoC's"
        verbose_name = "IoC"

    def __str__(self):
        return self.elastic_id
