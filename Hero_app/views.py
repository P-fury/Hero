from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView

from Hero_app.forms import CharCreateForm, ActivityTypeForm
from Hero_app.models import Char, ActivityType


# Create your views here.


class CharCreateView(CreateView):
    model = Char
    form_class = CharCreateForm
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



