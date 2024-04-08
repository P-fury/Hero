from collections import Counter, defaultdict
from datetime import datetime, timedelta
import math
from statistics import mean

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from Hero_app.forms import CharForm, ActivityTypeForm, ActivityForm, DayForm
from Hero_app.models import Char, ActivityType, Activity, Day, level_of_fatigue, mood_level, WeightIn
from Hero_app.matplot import get_plot

from django.utils import timezone


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
    success_url = reverse_lazy('char-page')


class DayView(ListView):
    model = Day
    template_name = 'day.html'
    context_object_name = 'day'


class EditDayView(UpdateView):
    model = Day
    template_name = 'edit_day.html'
    fields = ['date', 'mood', 'fatigue', 'note']
    success_url = reverse_lazy('char-page')


class CharPageView(View):
    def get(self, request):
        global remember_date
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

        """ACTIVITY COUNTER
        Args:
            activity_range: list of objects Day
        Returns:
            sorted dict of activities type and amount of them per week    
        """

        def activity_counter(activity_range):
            activity_dict = defaultdict(int)
            for day in activity_range:
                for activity in day.activity.all():
                    activity_dict[activity.activity_type.name] += 1
            return sorted(activity_dict.items(), key=lambda item: item[1], reverse=True)

        def daily_fatigue(activity_range):
            daily_fatigue_avg = defaultdict(list)
            for day in activity_range:
                fatigue = [activity.fatigue for activity in day.activity.all()]
                if fatigue:
                    date_key = day.date
                    daily_fatigue_avg[date_key] = mean(fatigue)
            return daily_fatigue_avg

        """MOOD AVERAGE COUNTER AND DESCRIPTION
        Args:
            summary: List of Day objects
            attribute_name: 'mood' or 'fatigue' attribute
            level_mapping: List of Choices 
        Returns:
            Text description of average mood or fatigue level or None
        """

        def calculate_avg_level(summary, attribute_name, level_mapping):
            levels = Counter(getattr(day, attribute_name) for day in summary if getattr(day, attribute_name))
            if levels:
                avg = sum(key * value for key, value in levels.items()) / sum(levels.values())
                avg_level_descrtiption = " ".join(
                    [f'{item}' for value, item in level_mapping if value == math.floor(avg) or value == math.ceil(avg)])
                return avg_level_descrtiption
            else:
                return None

        """Preparing variable for plotting function - get_plot
        Args:
            day_objects: List of object contains mood and workouts
        Returns:
            x for date,y for mood and z for workouts, ready to pass
        """

        def prep_data_for_plot(day_objects):
            x = [data.date.strftime("%d-%m") for data in day_objects]
            y = [data.mood for data in day_objects]
            sum_activity = []
            for day in day_objects:
                activity_count = day.activity.count()
                sum_activity.append(activity_count)
            z = sum_activity
            return x, y, z

        if request.GET.get('week_data'):
            last_added_day = days.last()
            week_data = last_added_day.date.weekday()
            start = last_added_day.date - timedelta(days=week_data)
            end = start + timedelta(days=6)
            days = days.filter(date__gte=start, date__lte=end)
            remember_date = start

        if request.GET.get('week_previous'):
            start = remember_date - timedelta(days=7)
            end = start + timedelta(days=6)
            days = days.filter(date__gte=start, date__lte=end)
            remember_date = start

        if request.GET.get('week_next'):
            start = remember_date + timedelta(days=7)
            end = start + timedelta(days=6)
            days = days.filter(date__gte=start, date__lte=end)
            remember_date = start

        context = {
            'char': char,
            'days': days,
            'activities': activities,
            'week_summary': week_summary,
            'month_summary': month_summary,
            'week_activity': activity_counter(week_summary),
            'month_activity': activity_counter(month_summary),
            'whole_activities': activity_counter(days),
            'daily_avg_fatigue_for_week': daily_fatigue(week_summary),
            'daily_avg_fatigue_for_month': daily_fatigue(month_summary),
            # 'daily_avg_fatigue': daily_fatigue(days),
            'avg_mood_week': calculate_avg_level(week_summary, "mood", mood_level),
            'avg_fatigue_week': calculate_avg_level(week_summary, "fatigue", level_of_fatigue),
            'avg_mood_month': calculate_avg_level(month_summary, "mood", mood_level),
            'avg_fatigue_month': calculate_avg_level(month_summary, "fatigue", level_of_fatigue),
            'avg_mood': calculate_avg_level(days, "mood", mood_level),
            'avg_fatigue': calculate_avg_level(days, "fatigue", level_of_fatigue),
            'weekly_chart': get_plot(prep_data_for_plot(week_summary)),
            'monthly_chart': get_plot(prep_data_for_plot(month_summary)),
            'all_data_chart': get_plot(prep_data_for_plot(days)),

        }
        return render(request, 'char_page.html', context
                      )

    def post(self, request):
        char = Char.objects.last()

        # ---- WEIGHT INS -------
        if 'weight_in' in request.POST:
            if request.POST['weight'] != '':
                WeightIn.objects.create(char=char, weight=request.POST['weight'])
                return HttpResponseRedirect(reverse_lazy('char-page'))
            else:
                return HttpResponseRedirect(reverse_lazy('char-page'))
        else:
            return HttpResponseRedirect(reverse_lazy('char-page'))
