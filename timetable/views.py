from django.shortcuts import render
from .models import Course, StudyHour
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
import pytz

day_num = {3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 1: 6, 2: 7}
day_nam = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
nam_day = {v: k for k, v in day_nam.items()}


# Create your views here.
def timetable(request):
    # timezone.activate(pytz.timezone('Canada/Eastern'))
    tz = timezone.get_current_timezone()
    context = {}

    week_days = [["Monday", "Mon"], ["Tuesday", "Tue"], ["Wednesday", "Wed"], ["Thursday", "Thu"], ["Friday", "Fri"],
                 ["Saturday", "Sat"], ["Sunday", "Sun"]]
    context['week_days'] = week_days
    courses = Course.objects.all()
    context['courses'] = courses

    now_canada = timezone.now().astimezone(tz=tz)
    now_weekday = now_canada.isoweekday()
    begin_of_week = now_canada - timedelta(days=now_weekday)
    begin_of_week = begin_of_week.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tz)
    last_of_week = begin_of_week + timedelta(days=7)
    last_of_week = last_of_week.replace(hour=23, minute=59, second=59, tzinfo=tz)
    query = StudyHour.objects.filter(start_time__gt=begin_of_week.astimezone(pytz.UTC))
    context['events'] = query

    context['from_date'] = begin_of_week
    context['to_date'] = last_of_week

    min_clock = last_of_week
    max_clock = begin_of_week

    if query.count() != 0:
        statistics = {}
        for event in query:
            if event.course_name.name in statistics:
                event_duration = event.end_time - event.start_time
                statistics[event.course_name.name][0] += event_duration
            else:
                event_duration = event.end_time - event.start_time
                statistics[event.course_name.name] = [event_duration, event.course_name.color]
            if timezone.localtime(event.start_time).hour < timezone.localtime(min_clock).hour:
                min_clock = event.start_time
            if timezone.localtime(event.end_time).hour > timezone.localtime(max_clock).hour:
                max_clock = event.end_time

        sum_hours = statistics[event.course_name.name][0]
        for key, val in statistics.items():
            sum_hours += val[0]
        sum_hours -= statistics[event.course_name.name][0]
        context['total_stats'] = sum_hours

        context['statistics'] = statistics
    else:
        context['total_stats'] = timedelta(0)
    if timezone.localtime(max_clock).hour > 24:
        context['clock_range'] = range(timezone.localtime(min_clock).hour, 25)
    else:
        context['clock_range'] = range(timezone.localtime(min_clock).hour, timezone.localtime(max_clock).hour + 2)
    context['table_height'] = 100 * (context['clock_range'][-1] - context['clock_range'][0] + 1)
    return render(request, template_name='timetable/base.html', context=context)


def timetable_past(request, week):
    context = {}

    week_days = [["Monday", "Mon"], ["Tuesday", "Tue"], ["Wednesday", "Wed"], ["Thursday", "Thu"], ["Friday", "Fri"],
                 ["Saturday", "Sat"], ["Sunday", "Sun"]]
    context['week_days'] = week_days

    context['past_week'] = week - 1
    context['next_week'] = week + 1

    courses = Course.objects.all()
    context['courses'] = courses

    now_weekday = timezone.now().isoweekday() - 1

    begin_of_week = (timezone.now() - timedelta(days=now_weekday)) - week * timedelta(
        days=7)
    begin_of_week = begin_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    last_of_week = begin_of_week + timedelta(days=7)
    query = StudyHour.objects.filter(Q(start_time__gte=begin_of_week) & Q(end_time__lte=last_of_week))
    context['events'] = query

    context['from_date'] = begin_of_week
    context['to_date'] = last_of_week

    min_clock = last_of_week
    max_clock = begin_of_week

    if query.count() != 0:
        statistics = {}
        for event in query:
            if event.course_name.name in statistics:
                event_duration = event.end_time - event.start_time
                statistics[event.course_name.name][0] += event_duration
            else:
                event_duration = event.end_time - event.start_time
                statistics[event.course_name.name] = [event_duration, event.course_name.color]
            if timezone.localtime(event.start_time).hour < timezone.localtime(min_clock).hour:
                min_clock = event.start_time
            if timezone.localtime(event.end_time).hour > timezone.localtime(max_clock).hour:
                max_clock = event.end_time

        sum_hours = statistics[event.course_name.name][0]
        for key, val in statistics.items():
            sum_hours += val[0]
        sum_hours -= statistics[event.course_name.name][0]
        context['total_stats'] = sum_hours

        context['statistics'] = statistics
    else:
        context['total_stats'] = timedelta(0)
    if timezone.localtime(max_clock).hour > 24:
        context['clock_range'] = range(timezone.localtime(min_clock).hour, 25)
    else:
        context['clock_range'] = range(timezone.localtime(min_clock).hour, timezone.localtime(max_clock).hour + 2)
    print(context['clock_range'][0], context['clock_range'][-1])
    context['table_height'] = 100 * (context['clock_range'][-1] - context['clock_range'][0] + 1)
    return render(request, template_name='timetable/base.html', context=context)
