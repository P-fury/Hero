from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView

from Hero_app.forms import CharForm, ActivityTypeForm, ActivityForm, DayForm
from Hero_app.models import Char, ActivityType, Activity, Day


# Create your views here.


class CharCreateView(CreateView):
    model = Char
    form_class = CharForm
    template_name = 'char.html'
    success_url = 'index'


class CharView(ListView):
    model = Char
    template_name = 'charview.html'
    context_object_name = 'character'


class index(View):
    def get(self, request):
        return render(request, 'index.html')


class AddActivityTypeView(CreateView):
    model = ActivityType
    form_class = ActivityTypeForm
    template_name = 'add_activity_type.html'
    success_url = 'index'
class ActivityTypesView(ListView):
    model = ActivityType
    template_name = 'activity_types.html'
    context_object_name = 'activity_types'

class AddActivityView(CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'add_activity.html'
    success_url = 'index'


class ActivityView(ListView):
    model = Activity
    template_name = 'activity_list.html'
    context_object_name = 'activities'


class AddDayView(CreateView):
    model = Day
    form_class = DayForm
    template_name = 'add_day.html'
    success_url = 'index'

class DayView(ListView):
    model = Day
    template_name = 'day.html'
    context_object_name = 'day'

