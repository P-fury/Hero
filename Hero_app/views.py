from datetime import datetime, timedelta
import math
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from Hero_app.forms import CharForm, ActivityTypeForm, ActivityForm, DayForm
from Hero_app.models import Char, ActivityType, Activity, Day ,level_of_fatigue,mood_level


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
        char = Char.objects.last()
        days = Day.objects.all().order_by('date')
        activities = Activity.objects.all()

        # --- WEEK COUNTER ----
        today = datetime.now()
        day_numb = today.weekday()
        start = today - timedelta(days=day_numb)
        end = start + timedelta(days=6)
        week_summary = days.filter(date__gte=start, date__lte=end)

        # ---- WEEK ACITIVITY COUNT ----
        week_activity = {}
        for day in week_summary:
            for activity in day.activity.all():
                if activity.activity_type.name not in week_activity:
                    week_activity[activity.activity_type.name] = 1
                else:
                    week_activity[activity.activity_type.name] += 1


        # ----- MOOD COUNTER and AVARAGE MOOD FOR WEEK (mood imported form models) ----
        def avg_mood_level(week_summary):
            week_mood = {}
            for day in week_summary:
                mood = day.mood # Pobieramy opis nastroju dla danego dnia
                if mood in week_mood:
                    week_mood[mood] += 1
                else:
                    week_mood[mood] = 1
            avg = sum(key * value for key,value in week_mood.items()) / sum(week_mood.values())
            avg_mood = " ".join([f'{item}' for value, item in mood_level if value == math.floor(avg) or value == math.ceil(avg)])
            return avg_mood

        #----- MOOD COUNTER and AVARAGE MOOD FOR WEEK (mood imported form models) ----
        def avg_fatigue_level(week_summary):
            week_fatigue = {}
            for day in week_summary:
                fatigue = day.fatigue
                if fatigue in week_fatigue:
                    week_fatigue[fatigue] += 1
                else:
                    week_fatigue[fatigue] = 1
            avg = sum(key * value for key, value in week_fatigue.items()) / sum(week_fatigue.values())
            avg_fatigue = " ".join(
                [f'{item}' for value, item in level_of_fatigue if value == math.floor(avg) or value == math.ceil(avg)])
            return avg_fatigue

        context = {
            'char': char,
            'days': days,
            'activities': activities,
            'week_summary': week_summary,
            'week_activity': week_activity,
            'avg_mood': avg_mood_level(week_summary),
            'avg_fatigue': avg_fatigue_level(week_summary),
        }
        return render(request, 'char_page.html', context
                      )
