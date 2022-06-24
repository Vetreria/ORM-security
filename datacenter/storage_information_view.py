from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime
from datacenter.models import get_duration, format_duration, is_visit_long
from datetime import timedelta


def storage_information_view(request):
    visitors_in_storage = Visit.objects.filter(leaved_at=None)
    serialized_visits = []
    for visit in visitors_in_storage:
        serialized_visits.append({
            'who_entered': visit.passcard.owner_name,
            'entered_at': visit.entered_at,
            'duration': format_duration(get_duration(visit)),
            'is_strange': is_visit_long(visit)
        })

    context = {
        'non_closed_visits': serialized_visits,
    }
    return render(request, 'storage_information.html', context)
