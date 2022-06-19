from django.db import models
from django.utils.timezone import localtime

def get_duration(visit):
    if visit.leaved_at is None:
        return localtime() - visit.entered_at
    return visit.leaved_at - visit.entered_at


def is_visit_long(visit, minutes=60):
    duration = get_duration(visit)
    total_minute = int(duration.total_seconds() // 60)
    return total_minute > minutes


def format_duration(duration_visit):
    total_seconds = duration_visit.total_seconds()
    total_hours = int(total_seconds // 3600)
    total_minute = int((total_seconds % 3600) // 60)
    return (f"{total_hours}:{total_minute:02}")


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )
