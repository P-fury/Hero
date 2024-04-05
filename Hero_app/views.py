from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from Hero_app.forms import CharForm, ActivityTypeForm, ActivityForm, DayForm
from Hero_app.models import Char, ActivityType, Activity, Day


# Create your views here.


class CharCreateView(CreateView):
    model = Char
    form_class = CharForm
    template_name = 'char.html'
    success_url = '/'


class CharView(ListView):
    model = Char
    template_name = 'charview.html'
    context_object_name = 'character'


class MainView(View):
    def get(self, request):
        return render(request, 'main.html')


class AddActivityTypeView(CreateView):
    model = ActivityType
    form_class = ActivityTypeForm
    template_name = 'add_activity_type.html'
    success_url = '/'


class ActivityTypesView(ListView):
    model = ActivityType
    template_name = 'activity_types.html'
    context_object_name = 'activity_types'


class AddActivityView(CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'add_activity.html'
    success_url = '/'


class ActivityView(ListView):
    model = Activity
    template_name = 'activity_list.html'
    context_object_name = 'activities'


class AddDayView(CreateView):
    model = Day
    form_class = DayForm
    template_name = 'add_day.html'
    success_url = '/'


class DayView(ListView):
    model = Day
    template_name = 'day.html'
    context_object_name = 'day'


class CharPageView(View):
    def get(self, request):
        today = datetime.now()
        day_numb = today.weekday()
        start = today - timedelta(days=day_numb)
        end = start + timedelta(days=6)

        char = Char.objects.last()
        days = Day.objects.all().order_by('date')
        week_summary = days.filter(date__gte=start, date__lte=end)
        activities = Activity.objects.all()
        return render(request, 'char_page.html',
                      {'char': char, 'days': days, 'activities': activities, 'week_summary': week_summary})
