from datetime import datetime, timedelta
import math
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from Hero_app.forms import CharForm, ActivityTypeForm, ActivityForm, DayForm
from Hero_app.models import Char, ActivityType, Activity, Day, level_of_fatigue, mood_level
from Hero_app.numpy import get_plot


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
        today = datetime.now()
        activities = Activity.objects.all()

        # --- WHOLE ACTIVITIES ---
        days = Day.objects.all().order_by('date')

        # ---- MONTH COUNTER ----
        today_month = today.month
        month_summary = days.filter(date__month=today_month)

        # --- WEEK COUNTER ----
        day_numb = today.weekday()
        start = today - timedelta(days=day_numb)
        end = start + timedelta(days=6)
        week_summary = days.filter(date__gte=start, date__lte=end)

        # ---- WEEK ACITIVITY COUNT ----
        def activity_counter(activity_range):
            activity_dict = {}
            for day in activity_range:
                for activity in day.activity.all():
                    if activity.activity_type.name not in activity_dict:
                        activity_dict[activity.activity_type.name] = 1
                    else:
                        activity_dict[activity.activity_type.name] += 1
            return activity_dict

        # ----- MOOD COUNTER and AVARAGE MOOD FOR WEEK (mood imported form models) ----
        def avg_mood_level(summary):
            mood_dict = {}
            for day in summary:
                if day.mood:
                    mood = day.mood
                    if mood in mood_dict:
                        mood_dict[mood] += 1
                    else:
                        mood_dict[mood] = 1
            if mood_dict:
                avg = sum(key * value for key, value in mood_dict.items()) / sum(mood_dict.values())
                avg_mood = " ".join(
                    [f'{item}' for value, item in mood_level if value == math.floor(avg) or value == math.ceil(avg)])
                return avg_mood

        # ----- MOOD COUNTER and AVARAGE MOOD FOR WEEK (mood imported form models) ----
        def avg_fatigue_level(summary):
            fatigure_dict = {}
            for day in summary:
                if day.fatigue:
                    fatigue = day.fatigue
                    if fatigue in fatigure_dict:
                        fatigure_dict[fatigue] += 1
                    else:
                        fatigure_dict[fatigue] = 1
            if fatigure_dict:
                avg = sum(key * value for key, value in fatigure_dict.items()) / sum(fatigure_dict.values())
                avg_fatigue = " ".join(
                    [f'{item}' for value, item in level_of_fatigue if
                     value == math.floor(avg) or value == math.ceil(avg)])
                return avg_fatigue

        # day_lst = [day.date.weekday() for day in week_summary]
        # x = [data.date for data in week_summary]
        # y = [data.activity for data in week_summary.activity.all]
        # print(x)
        # print(y)
        # weekly_chart = get_plot(x, y)

        context = {
            'char': char,
            'days': days,
            'activities': activities,
            'week_summary': week_summary,
            'month_summary': month_summary,
            'week_activity': activity_counter(week_summary),
            'month_activity': activity_counter(month_summary),
            'whole_activities': activity_counter(days),
            'avg_mood_week': avg_mood_level(week_summary),
            'avg_fatigue_week': avg_fatigue_level(week_summary),
            'avg_mood_month': avg_mood_level(month_summary),
            'avg_fatigue_month': avg_fatigue_level(month_summary),
            'avg_mood': avg_mood_level(days),
            'avg_fatigue': avg_fatigue_level(days),
            # 'weekly_chart': weekly_chart,
        }
        return render(request, 'char_page.html', context
                      )
